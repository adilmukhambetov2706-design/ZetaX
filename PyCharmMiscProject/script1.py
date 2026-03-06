#import requests
import customtkinter as ctk

api_key = 'd57a3845315ffcc38df8af6af61ffb9c'


#weather_data = requests.get(
#    f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}&units=metric")

#weather = weather_data.json()['weather'][0]['main']
#temp = weather_data.json()['main']['temp']

#print(weather, temp)

class Weather(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x1000")
        self.title("ZetaX")
        self.city = ctk.CTkEntry(self, placeholder_text="Enter City", width=300, height=40)
        self.city.pack(anchor="n", padx=20, pady=20)


wea = Weather()
wea.mainloop()