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

import customtkinter
from tkintermapview import TkinterMapView
from PIL import Image
import weathercurrent
import weatherforecast
import json
import os




class UI(customtkinter.CTk):

    APP_NAME = "The Weather App"
    DEFAULT_MODE = "System"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window = customtkinter.CTk()
        self.title(UI.APP_NAME)
        self.geometry(f"{1080}x{720}")
        self.minsize(1080,720)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        self.marker_list = []

        imgfile_path = os.path.join(r"./icons/smiley.png")

        # ================Main Frame creation for side bar and map widget===============#

        # Create Map Frame
        self.frameMap = customtkinter.CTkFrame(master=self, width=700, height=700, corner_radius= 10)
        self.frameMap.pack(side="right", fill="both", pady=10,padx=10, expand=True)

        # Create SideBar Frame
        self.frameSide = customtkinter.CTkFrame(master=self, width=300, height=400, corner_radius= 10)
        self.frameSide.pack(side="left",fill="both", padx=10, pady=10, expand=True)

        # ================Main Frame creation for side bar and map widget===============#


        # ================ Create text entry bar and button to search for location by name =================#

        # Create EntryBar Frame.
        self.frameEntry = customtkinter.CTkFrame(master=self.frameMap, width=700, height=30, fg_color="transparent")
        self.frameEntry.pack(side="top",fill="x",padx=(1,0))

        # Create Entry Bar for text input
        self.entry = customtkinter.CTkEntry(master=self.frameEntry, placeholder_text="Type Location", width=240)
        self.entry.pack(side="left", anchor="center")
        self.entry.bind('<Return>', self.search_event)

        # Create SearchButton for the confirmation of the search input
        self.buttonSearch = customtkinter.CTkButton(master=self.frameEntry, text="Search", width=90,command=self.search_event)
        self.buttonSearch.pack(side="left", anchor="center")

        # ================ Create text entry bar and button to search for location by name =================#


        # =============== Creation of map widget with setmarkerevent ===============#

        # Setup Map Frame
        self.map_widget = TkinterMapView(master=self.frameMap, width=700, height=700)
        self.map_widget.pack(expand=True, fill="both",side="bottom")
        self.map_widget.add_right_click_menu_command(label="Add Marker", command=self.set_marker_event, pass_coords=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # =============== Creation of map widget with setmarkerevent ===============#

        # =============Main weather icon frame and object loading================#

        #Create frame for location name
        self.frameLocName = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent")
        self.frameLocName.pack(side="top", anchor="center", pady=(10,0))
        self.locNameLabel = customtkinter.CTkLabel(master=self.frameLocName, fg_color="transparent", font=("Seoge UI",14, 'bold'), text="")
        self.locNameLabel.pack(side="top", anchor="center")

        # Create Frame for weather icon.
        self.frameWeatherIcon = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent",width=100, height=100)
        self.frameWeatherIcon.pack(side="top", anchor="n")


        # Create Image obj.
        self.weatherIcon_Label = customtkinter.CTkLabel(master=self.frameWeatherIcon,text="",
                                                        fg_color="transparent")
        self.weatherIcon_Label.pack(side="top", anchor="n")

        # =============Main weather icon frame and object loading================#


        # =============Frame for Weather Data and stuff=============#

        # #Create Frame for weather data.
        self.frameCondTemp = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent",height=50, width=150)
        self.frameCondTemp.pack(side="top", anchor="center")
        self.weatherCond = customtkinter.CTkLabel(master=self.frameCondTemp, fg_color="transparent", font=("Seoge UI", 20, 'bold'), text="")
        self.weatherTemp = customtkinter.CTkLabel(master=self.frameCondTemp, fg_color="transparent", font=("Seoge UI", 14,'bold'), text="")
        self.weatherCond.pack(side="top", anchor="n")
        self.weatherTemp.pack(side="top", anchor="n")

        # #Create frame for Humidity text and icon.
        self.weatherHumidityFrame = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent", height=20, width=150)
        self.weatherHumidityFrame.pack_propagate(0)
        self.weatherHumidityFrame.pack(side="top", anchor="center")

        # #Instert Humidity Data into frame.
        # self.HumidityIcon = customtkinter.CTkImage(light_image=Image.open(r"C:\Users\derst\Desktop\ERGASIES EAP\PyProjects\WeatherProject\icons\humid.png"),size=(50,50))
        self.weatherHumidityData = customtkinter.CTkLabel(master=self.weatherHumidityFrame, fg_color="transparent", font=("Seoge UI", 12), text=(""))
        self.weatherHumidityData.pack(side="left", anchor="center",padx=(15,0))
        self.weatherHumidFrame = customtkinter.CTkLabel(master=self.weatherHumidityFrame, fg_color="transparent", text="")
        self.weatherHumidFrame.pack(side="left", anchor="center")

        # #Create Label for other data.
        self.frameOtherData = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent", width=200, height=50)
        self.frameOtherData.pack(side="top", anchor="center")
        self.weatherOtherData = customtkinter.CTkLabel(master=self.frameOtherData, fg_color="transparent", font=("Seoge UI", 12), text="")
        self.weatherOtherData.pack(side="top", anchor="center")

        # =============Frame for Weather Data and stuff=============#



        # # Create Frame for Scrollable widget.
        self.frameScrollable = customtkinter.CTkScrollableFrame(master=self.frameSide, orientation="horizontal",
                                                                width=300, height=325)
        self.frameScrollable.pack(side="top", anchor="center", fill="x", pady=(15, 0))
        self.WrapperFrameScrollable = customtkinter.CTkFrame(master=self.frameScrollable, fg_color="white")
        self.WrapperFrameScrollable.pack(anchor="center", fill="both",expand=True)



        # ================ Creation of appearance and tile change option menus ====================#

        # Create Labels and Buttons for appearance and tile change.
        self.settingsOptionFrame = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent")
        self.settingsOptionFrame.pack(side="bottom", fill="x",padx=10, pady=(0,10))
        self.settingsAppearLabelFrame = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent", width=150)
        self.settingsAppearLabelFrame.pack(side="left", anchor="s", pady=0)
        self.settingsTileLabelFrame = customtkinter.CTkFrame(master=self.frameSide, fg_color="transparent",width=150)
        self.settingsTileLabelFrame.pack(side="right", anchor="s", pady=0)

        self.changeAppearance = customtkinter.CTkLabel(master=self.settingsAppearLabelFrame, fg_color="transparent", font=("Seoge UI",12), text="Appearance Mode",width=150)
        self.changeAppearance.pack(side="left", anchor="center")


        self.changeTiles = customtkinter.CTkLabel(master=self.settingsTileLabelFrame, fg_color="transparent", font=("Seoge UI", 12), text="Tile Mode",width=150)
        self.changeTiles.pack(side="left", anchor="center")



        self.AppearanceOptionMenu = customtkinter.CTkOptionMenu(master=self.settingsOptionFrame, values=["Light","Dark"], command=self.change_appearance_mode)
        self.AppearanceOptionMenu.pack(side="left",anchor="w")
        self.TileOptionMenu = customtkinter.CTkOptionMenu(master=self.settingsOptionFrame, values=["OpenStreetMap", "Google Normal", "Google Satellite"], command=self.change_map)
        self.TileOptionMenu.pack(side="right", anchor="e")

        self.map_widget.set_address("Athens,Greece")
        self.TileOptionMenu.set("Google Normal")
        self.AppearanceOptionMenu.set("Dark")

        # ================ Creation of appearance and tile change option menus ====================#
        self.on_startup()


    def on_startup(self):
        self.marker_list.append((37.9731438, 23.7292122))
        self.get_data()
        self.get_forecast()
        self.del_marker_list()
    def set_marker_event(self, coords):
        self.del_marker_list()
        new_marker = self.map_widget.set_marker(coords[0], coords[1])
        self.marker_list.append((coords[0], coords[1]))
        self.get_data()
        self.get_forecast()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def get_data(self):

        marker_tuple = self.marker_list[0]
        marker_string = ','.join(map(str, marker_tuple))

        lat_str, lon_str = marker_string.split(',')
        latitude = float(lat_str.strip())
        longitude = float(lon_str.strip())



        # Create an instance of WeatherCurrent with the provided latitude and longitude
        data = weathercurrent.WeatherCurrent(latitude, longitude)
        # Call the method to get weather data for the provided coordinates
        data.get_weather_data()

        # Get the directory of the current Python script
        jscript_dir = os.path.dirname(os.path.abspath(__file__))

        # Specify the subdirectory and filename for the JSON file
        jsubdirectory = 'weatherdata'

        jfile_name = 'curr_weather.json'

        # Construct the full path to the JSON file
        json_file_path = os.path.join(r"./weatherdata/",jfile_name)
        # Export data to JSON
        with open(json_file_path, 'r') as file:
            curr_weather_data = json.load(file)

        # Define the directory where PNG files are located
        imgpath_dir = os.path.join(r'./icons/')


        # Get a list of all files in the directory
        file_list = os.listdir(r"./icons")

        # Check if the icon variable name matches any PNG file name
        icon_file_path = None
        for file in file_list:
            # Remove the file extension to compare with the icon variable
            if os.path.splitext(file)[0] == curr_weather_data['icon']:
                # Construct the full path to the icon file
                icon_file_path = os.path.join(imgpath_dir, file)
                break



        # =============Frame for Weather Data and stuff=============#
        # =============Main weather icon frame and object loading================#
        self.frameLocName.pack_configure(side="top",anchor="center")
        self.locNameLabel.configure(text=f"The weather in {curr_weather_data['location']}")
        # Create Image obj.
        self.weatherIcon = customtkinter.CTkImage(light_image=Image.open(rf'{icon_file_path}'),size=(100,100))
        self.weatherIcon_Label.configure(image=self.weatherIcon)
        # =============Main weather icon frame and object loading================#

        self.weatherCond.configure(text=f"{curr_weather_data['status']}")
        self.weatherTemp.configure(text=f"Temperature \n{curr_weather_data['temperature']['current']}°C")

        #Instert Humidity Data into frame.
        self.HumidityIcon = customtkinter.CTkImage(light_image=Image.open(r".\icons\humid.png"),size=(50,50))
        self.weatherHumidityData.configure(text=(f"{curr_weather_data['humidity']}% Humidity "))
        self.weatherHumidityData.pack_configure(side="left", anchor="center")
        self.weatherHumidFrame.configure(image=self.HumidityIcon)

        #Create Label for other data.
        self.weatherOtherData.configure(text=(f"Wind Speed: {curr_weather_data['wind']['speed']} "
                                             f"m/s   Direction: {curr_weather_data['wind']['direction']}"
                                             f"\nSunrise: {curr_weather_data['sunrise']} "
                                             f"   Sunset: {curr_weather_data['sunset']}"))



        # =============Frame for Weather Data and stuff=============#

    def get_forecast(self):
        marker_tuple = self.marker_list[0]
        marker_string = ','.join(map(str, marker_tuple))

        lat_str, lon_str = marker_string.split(',')
        latitude = float(lat_str.strip())
        longitude = float(lon_str.strip())

        forecast = weatherforecast.WeatherForecast(latitude, longitude)

        forecast.get_forecast_data()

        jfile_name = 'forecast_weather.json'

        # Construct the full path to the JSON file
        json_file_path = os.path.join(r"./weatherdata/", jfile_name)
        # Export data to JSON
        with open(json_file_path, 'r') as file:
            forecast_weather = json.load(file)


        # Define the directory where PNG files are located
        imgpath_dir = os.path.join(r'./icons/')

        # Get a list of all files in the directory
        file_list = os.listdir(r"./icons")

        self.WrapperFrameScrollable.destroy()
        self.WrapperFrameScrollable = customtkinter.CTkFrame(master=self.frameScrollable, fg_color="transparent")
        self.WrapperFrameScrollable.pack(anchor="center", fill="both", expand=True)

        # ========= POPULATING SCROLLABLE ========= #
        for index, entry in enumerate(forecast_weather):
            icon_file_path = None
            for file in file_list:
                # Remove the file extension to compare with the icon variable
                if os.path.splitext(file)[0] == entry['icon']:
                    # Construct the full path to the icon file
                    icon_file_path = os.path.join(imgpath_dir, file)
                    break

                # Create unique variable names based on index number
            populant_frame_name = f"populantFrame_{index}"
            forecast_time_name = f"forecastTime_{index}"
            forecast_img_name = f"forecastImg_{index}"
            forecast_img_label_name = f"forecastImgLabel_{index}"
            forecast_cond_name = f"forecastCond_{index}"
            forecast_temp_name = f"forecastTemp_{index}"
            forecast_humidity_icon_name = f"forecastHumidityIcon_{index}"
            forecast_humidity_frame_name = f"forecastHumidityFrame_{index}"
            forecast_humidity_data_name = f"forecastHumidityData_{index}"
            forecast_humidity_icon_frame_name = f"forecastHumidityIconFrame_{index}"
            forecast_other_data_name = f"forecastOtherData_{index}"

            # Create widgets with unique variable names
            setattr(self, populant_frame_name,
                    customtkinter.CTkFrame(master=self.WrapperFrameScrollable, fg_color="transparent", width=200,
                                           border_width=2, border_color="grey", corner_radius=5))
            getattr(self, populant_frame_name).pack(side="left", anchor="e",fill="y", padx=5)
            setattr(self, forecast_time_name,
                    customtkinter.CTkLabel(master=getattr(self, populant_frame_name), fg_color="transparent",
                                           font=("Seoge UI", 12), text=f"{entry['time']}"))
            getattr(self, forecast_time_name).pack(side="top", anchor="n",pady=(7.5,0))
            setattr(self, forecast_img_name,
                    customtkinter.CTkImage(light_image=Image.open(rf"{icon_file_path}"), size=(100, 100)))
            setattr(self, forecast_img_label_name, customtkinter.CTkLabel(master=getattr(self, populant_frame_name),
                                                                          image=getattr(self, forecast_img_name),
                                                                          fg_color="transparent", text=""))
            getattr(self, forecast_img_label_name).pack(side="top", anchor="n",padx=10)
            setattr(self, forecast_cond_name,
                    customtkinter.CTkLabel(master=getattr(self, populant_frame_name), fg_color="transparent",
                                           font=("Seoge UI", 14),
                                           text=f"{entry['status']}"))
            getattr(self, forecast_cond_name).pack(side="top", anchor="n")
            setattr(self, forecast_temp_name,
                    customtkinter.CTkLabel(master=getattr(self, populant_frame_name), fg_color="transparent",
                                           font=("Seoge UI", 14),
                                           text=f"Temperature\n{entry['temperature']['current']}°C"))
            getattr(self, forecast_temp_name).pack(side="top", anchor="n")
            setattr(self, forecast_humidity_icon_name, customtkinter.CTkImage(light_image=Image.open(
                r".\icons\humid.png"),
                                                                              size=(50, 20)))
            setattr(self, forecast_humidity_frame_name,
                    customtkinter.CTkFrame(master=getattr(self, populant_frame_name), fg_color="transparent",
                                           height=20, width=150))
            setattr(self, forecast_humidity_data_name,
                    customtkinter.CTkLabel(master=getattr(self, populant_frame_name),
                                           fg_color="transparent",
                                           font=("Seoge UI", 12), text=(f"{entry['humidity']}% Humidity")))
            getattr(self, forecast_humidity_data_name).pack(side="top", anchor="center")
            getattr(self, forecast_humidity_frame_name).pack(side="top", anchor="center")
            setattr(self, forecast_humidity_icon_frame_name,
                    customtkinter.CTkLabel(master=getattr(self, forecast_humidity_frame_name),
                                           fg_color="transparent",
                                           text="", image=getattr(self, forecast_humidity_icon_name)))
            getattr(self, forecast_humidity_icon_frame_name).pack(side="left", anchor="center")
            setattr(self, forecast_other_data_name,
                    customtkinter.CTkLabel(master=getattr(self, populant_frame_name), fg_color="transparent",
                                           font=("Seoge UI", 12),
                                           text=(
                                               f"Wind speed \n{entry['wind']['speed']}m/s\n\nDirection: {entry['wind']
                                               ['direction']}")))
            getattr(self, forecast_other_data_name).pack(side="top", anchor="center")




    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google Normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
        elif new_map == "Google Satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
    def search_event(self, event=None):
        self.del_marker_list()
        self.map_widget.set_address(self.entry.get())
        current_position = self.map_widget.get_position()
        self.map_widget.set_marker(current_position[0], current_position[1])
        self.marker_list.append((current_position[0], current_position[1]))
        self.get_data()
        self.get_forecast()

    def del_marker_list(self):
        if len(self.marker_list) == 1:
            del self.marker_list[0]
            self.map_widget.delete_all_marker()

    def on_closing(self, event=0):
        self.destroy()
    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = UI()
    app.start()