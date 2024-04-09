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
from datetime import datetime


class WeatherForecast:
    def __init__(self, latitude, longitude):
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



    def get_forecast_data(self):
        # Get forecast data
        forecaster = self.mgr.forecast_at_coords(self.latitude, self.longitude, '3h')


        if forecaster is not None:
            # Initialize an empty list to store forecast entries
            forecast_weather = []

            # Iterate over forecast entries
            for weather in forecaster.forecast:

                # Convert wind direction from degrees to compass direction
                compass_direction = self.deg_to_direction(weather.wind()['deg'])

                # Convert reference time to datetime object
                ref_time = datetime.fromtimestamp(weather.reference_time())

                # Format reference time to include only month, day, hour, and minute
                formatted_time = ref_time.strftime('%m-%d %H:%M')

                # Create a dictionary for each forecast entry
                forecast_entry = {
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
                    'time': formatted_time  # Formatted reference time
                }

                # Append the forecast entry to the list
                forecast_weather.append(forecast_entry)

            # Get the directory of the current Python script
            jscript_dir = os.path.dirname(os.path.abspath(__file__))

            # Specify the subdirectory and filename for the JSON file
            subdirectory = 'weatherdata'
            jfile_name = 'forecast_weather.json'

            # Construct the full path to the JSON file
            json_file_path = os.path.join(jscript_dir, subdirectory, jfile_name)

            # Export data to JSON
            with open(json_file_path, 'w') as json_file:
                json.dump(forecast_weather, json_file, indent=4)

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
            return f"{location.name}"  # , {location.country}
        return None


