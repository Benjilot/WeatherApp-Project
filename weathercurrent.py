"""
WeatherApp, GUI App to get weather info based on location.
Copyright (C) 2024 Benjilot

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Import necessary modules
from pyowm.owm import OWM
import json
import os
from timezonefinder import TimezoneFinder
from pytz import timezone

class WeatherCurrent:
    def __init__(self, latitude, longitude):
        # Initialize with latitude and longitude
        self.latitude = latitude
        self.longitude = longitude

        # Read API key from file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = 'APIkey.txt'
        api_key_file_path = os.path.join(script_dir, file_name)
        with open(api_key_file_path) as file:
            api_key = file.read().strip()

        # Store API key and initialize OWM manager
        self.api_key = api_key
        self.owm = OWM(api_key)
        self.mgr = self.owm.weather_manager()
        self.revgeo = self.owm.geocoding_manager()

    def get_weather_data(self):
        # Get weather data based on coordinates
        observation = self.mgr.weather_at_coords(self.latitude, self.longitude)

        if observation is not None:
            # Retrieve weather information
            weather = observation.weather

            # Get local timezone
            tf = TimezoneFinder()
            local_timezone = tf.timezone_at(lng=self.longitude, lat=self.latitude)
            local_timezone = timezone(local_timezone)

            # Convert sunrise and sunset times to local time
            sunrise = weather.sunrise_time('date')
            sunset = weather.sunset_time('date')
            sunrise_local = sunrise.astimezone(local_timezone)
            sunset_local = sunset.astimezone(local_timezone)

            # Convert wind direction from degrees to compass direction
            compass_direction = self.deg_to_direction(weather.wind()['deg'])

            # Get location name
            locname = self.get_location_name(self.latitude, self.longitude)

            # Create dictionary for current weather data
            curr_weather = {
                'location': locname,
                'status': weather.status,
                'icon': weather.weather_icon_name,
                'temperature': {
                    'current': round(weather.temperature('celsius')['temp'])
                },
                'humidity': weather.humidity,
                'wind': {
                    'speed': weather.wind()['speed'],
                    'direction': compass_direction
                },
                'sunrise': sunrise_local.strftime('%H:%M'),
                'sunset': sunset_local.strftime('%H:%M')
            }

            # Get the directory of the current Python script
            jscript_dir = os.path.dirname(os.path.abspath(__file__))

            # Specify the subdirectory and filename for the JSON file
            subdirectory = 'weatherdata'
            jfile_name = 'curr_weather.json'

            # Construct the full path to the JSON file
            json_file_path = os.path.join(jscript_dir, subdirectory, jfile_name)

            # Export data to JSON
            with open(json_file_path, 'w') as json_file:
                json.dump(curr_weather, json_file, indent=4)

    def deg_to_direction(self, degrees):
        # Convert wind direction in degrees to compass direction
        compass_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                              'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return compass_directions[index]

    def get_location_name(self, latitude, longitude):
        # Reverse geocode to get the location name
        result = self.revgeo.reverse_geocode(latitude, longitude, limit=1)
        if result:
            location = result[0]
            return f"{location.name}" #, {location.country}
        return None
