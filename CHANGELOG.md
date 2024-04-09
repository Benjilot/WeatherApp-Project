# Changelog

## 04/04/2024 - 05/04/2024

1. Creation of the base layout of the app with CustomTKinter frames.

1. Implementation of the MapView widget with the TKinterMapView library.

1. Implementation of all the frames and widgets that contain the weather data. Fixed alignment and .pack() priority. They all use placeholder images and texts. Made with CustomTKinter.

1. Implementation of the appearance and tile change buttons and labels along with functions to make the requested changes on the window.

1. Implementation of the text box and the search button. Made functions to connect with MapView widget so the location changes on user input. Parses tuple with coordinates in marker_list[].
Also made function so that the user can press "Enter" to give input instead of always having to press the Search button.


1. Implementation of a function that makes a menu pop up when right clicking on the map. Added "Add Marker" option in the menu. Gets position of the mouse and parses the tuple to marker_list[]


## 07/04/2024

1. Made weathercurrent.py using PYOWM library. Implemented way to call the OpenWeatherMapAPI.
Read API key from the APIkey.txt file. 

1. Implemented function that gets the current weather for the given coordinates.
Makes a json file named curr_weather.json and exports only the requested data into that file.

1. Made a function that converts the time to the local time based on the coordinates using datetime,pytz,timezonefinder libraries because OpenWeatherMap always uses UTC time.

1. Made a function that converts the degrees of the wind direction into compass direction (e.g N,NE).

1. Also made function that gets the location name using reverse_geocode from PYOWM.

1. Implemented the connection of the weathercurrent.py in the weatherui.py file.

1. Changed the creation of the base frames so that they initialy pack empty but kept the desired alignment and render order.

1. Made a function named get_data to pass the coordinates of the desired location to the WeatherCurrent class from the weathercurrent.py file and update the base frames and widgets so that they dynamically change with the data in the curr_weather.json file. 

1. Made the initial location of the app to be Athens,GR so that the frames aren't empty on startup. Made a function on startup that calls the get_data func to get weather info for Athens.

1. Changed the marker functions so that they call the get_data function as soon as a marker is placed down.


## 08/04/2024

1. Made weatherforecast.py using the PYOWM library. Implemented way to call the OpenWeatherMapAPI and read API key from the APIkey.txt file.

1. Implemented function that gets the 3 hour interval forecast of the given coordinates.
Makes a json file name forecast_weahter.json and exports requested data into it.

1. Also made a way to format the request date and time so that the json only keeps the month day and time of the data list (e.g. 20-10 4:00) using datetime library.

1. Implemented the connection of the weatherforecast.py in the weatherui.py file.

1. Made function called get_forecast that gets the requested data for the given coordinates.

1. Implemented a way in the function to dynamically populate the initial scrollable frame with wrapper frames that contain all of the information of the forecast. Each frame and widget has a different in them so that there's no problems with the pack order and renders. 

1. Made it so that every time the get_forecast function is called the wrapper frame that contains all the frames and widgets for the forecast data gets destroyed and remade.

1. Made it so that the get_forecast function gets called on startup as well.

1. Refined the overall alignment and look of the UI so that it doesn't look as bad as it was before. Made sure everything works and looks good after giving coordinates and requesting data a lot times.




