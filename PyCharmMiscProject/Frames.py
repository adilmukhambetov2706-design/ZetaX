from customtkinter import *
from PIL import Image
import requests
from datetime import datetime, timedelta

API_KEY = "d57a3845315ffcc38df8af6af61ffb9c"
mb = 'Montserrat SemiBold'
m = 'Montserrat'
tr = 'transparent'
url = f"https://api.openweathermap.org/data/2.5/forecast?q=Bishkek&units=metric&appid={API_KEY}"
weather_data = requests.get(url).json()



class Upper_frame(CTkFrame):
    def __init__(self, master, n):
        super().__init__(master, width=1293, height=40, fg_color=tr)
        color = "#D9D9D9"

        CTkLabel(self, text='Zeta-X', font=(mb, 32)).grid(column=0, row=0, padx=52)

        search_frame = CTkFrame(self, width=600, height=34, corner_radius=17, fg_color=color)
        search_frame.grid(column=1, row=0, padx=(110, 0))

        CTkLabel(search_frame, image=CTkImage(Image.open("Icons/Search.png"),
                                              size=(24, 24)), text="").grid(column=0, row=0, padx=(20, 0))

        self.search_entry = CTkEntry(search_frame, placeholder_text="Search", corner_radius=17, border_color=color,
                                fg_color=color, text_color="#000000", placeholder_text_color='#422BA0', width=671, height=34)
        self.search_entry.grid(column=1, row=0, padx=(0, 100))

        burger_image = CTkImage(light_image=Image.open('Icons/menu.png'), size=(58, 42))
        burger_button = CTkButton(self, image=burger_image, height=42, width=58, fg_color=tr,
                                  text="")
        burger_button.grid(column=n, row=0, padx=60)



class Middle_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1344, height=619, fg_color="#161358",
                         corner_radius=15, border_color="#FFFFFF", border_width=1)

        kroshki_frame = CTkFrame(self, fg_color=tr)
        kroshki_frame.pack(anchor='nw', pady=(23, 0), padx=25)
        CTkLabel(kroshki_frame, text="Home", font=(mb, 14)).grid(column=0, row=0)
        chevron_image = CTkImage(Image.open('Icons/chevron.png'), size=(24, 24))
        CTkLabel(kroshki_frame, image=chevron_image, text="").grid(column=1, row=0, padx=14)
        CTkLabel(kroshki_frame, text="Bishkek", font=(mb, 14)).grid(column=2, row=0)

        CTkLabel(self, text='Bishkek: Detailed 14-Day & Hourly Forecast',
                 font=(m, 48)).pack(anchor='n', pady=(33, 0))

        detailed_24h_frame = CTkFrame(self, fg_color=tr, width=1292, corner_radius=15)
        detailed_24h_frame.pack(anchor='n', pady=(42, 0), padx=(1, 1))

        CTkLabel(detailed_24h_frame, text='Bishkek: Detailed (24 Hours)',
                  font=(mb, 24)).pack(anchor='n', pady=(15, 0))

        hourly_time_frame = CTkFrame(detailed_24h_frame, fg_color=tr)
        hourly_time_frame.pack(anchor="n", pady=(60, 0), padx=(39, 0))

        timezone_offset = weather_data['city']['timezone']
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(seconds=timezone_offset)
        for i in range(8):
            hour_time = local_time + timedelta(hours=i)
            CTkLabel(hourly_time_frame, text=f"{hour_time.hour:02d}:00", font=(mb, 32)).grid(column=i, row=0, padx=(0, 84))

            weather = weather_data['list'][i//3]['weather'][0]['main']
            weather_image = CTkImage(Image.open(f"Second/Weathers/{weather}.png"), size=(80, 80))
            CTkLabel(hourly_time_frame, image=weather_image, text="").grid(column=i, row=1, padx=(0, 84), pady=(12, 0))


            city_temp = weather_data['list'][i//3]['main']['temp']
            CTkLabel(hourly_time_frame, text=f"{int(city_temp)}°C", font=(m, 24)).grid(column=i, row=2, padx=(0, 84), pady=(12, 0))


class Lower_Frame(CTkFrame):
    def __init__(self, master):
        font = CTkFont(m, 24)
        font_semibold = CTkFont(mb, 28)
        pady=(30, 0)
        color = "#B8B7CF"
        super().__init__(master, width=1344, height=431, fg_color="#130F60", corner_radius=15,
                         border_color="#FFFFFF", border_width=1)

        CTkLabel(self, text='Day', text_color=color, font=font_semibold).grid(column=0, row=0, padx=(21, 0), pady=pady)
        CTkLabel(self, text='Date', text_color=color, font=font_semibold).grid(column=1, row=0, padx=(76, 0), pady=pady)
        CTkLabel(self, text='Weather', text_color=color, font=font_semibold).grid(column=2, row=0, padx=(80, 0), pady=pady)
        CTkLabel(self, text='', width=207).grid(column=3, row=0,pady=pady)
        CTkLabel(self, text='Min / Max', text_color=color, font=font_semibold).grid(column=4, row=0, pady=pady)
        CTkLabel(self, text='UV Index', text_color=color, font=font_semibold).grid(column=5, row=0, padx=(78, 0), pady=pady)
        CTkLabel(self, text='Humidity', text_color=color, font=font_semibold).grid(column=6, row=0, padx=(81, 23), pady=pady)

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        pady=(1, 0)
        color = "#FFFFFF"

        for i in range(5):
            today = datetime.now()
            day = today + timedelta(days=i)
            CTkLabel(self, text=day.strftime("%a"), text_color=color, font=font).grid(column=0, row=i + 1, pady=pady)

            timezone_offset = weather_data['city']['timezone']
            utc_now = datetime.utcnow()
            local_time = utc_now + timedelta(seconds=timezone_offset)
            date = local_time + timedelta(days=i)
            CTkLabel(self, text=f"{months[date.month-1]} {date.day}",
                     text_color=color, font=font).grid(column=1, row=i + 1, pady=pady)

            weather_frame = CTkFrame(self, fg_color=tr)
            weather_frame.grid(column=2, row=i + 1, pady=pady)

            weather = weather_data['list'][i*8]['weather'][0]['main']
            weather_image = CTkImage(Image.open(f"Second/Weathers/{weather}.png"), size=(56, 56))
            CTkLabel(weather_frame, image=weather_image, text="").grid(column=0, row=0)
            CTkLabel(weather_frame, text=weather, text_color=color, font=font).grid(column=1, row=0)

            temps = []
            for j in range(8):
                index = i * 8 + j
                if index < len(weather_data["list"]):
                    temps.append(weather_data["list"][index]["main"]["temp"])

            min_temp = int(min(temps))
            max_temp = int(max(temps))
            if i == 0:
                CTkLabel(self, text=f"{min_temp}°/{max_temp}°", text_color=color, font=font).grid(column=4, row=i+1, pady=pady)
            else:
                min_max_frame = CTkFrame(self, fg_color=tr)
                min_max_frame.grid(column=4, row=i + 1, pady=pady)
                CTkLabel(min_max_frame, text=f"{min_temp}°", text_color="#0699D7", font=font).grid(column=0, row=0)
                CTkLabel(min_max_frame, text="/", text_color=color, font=font).grid(column=1, row=0)
                CTkLabel(min_max_frame, text=f"{max_temp}°", text_color="#FF5A5A", font=font).grid(column=2, row=0)


            CTkLabel(self, text="N/A", text_color=color, font=font).grid(column=5, row=i+1, pady=pady)

            humidity = weather_data["list"][i*5]["main"]["humidity"]
            CTkLabel(self, text=f"{humidity}%", text_color=color, font=font).grid(column=6, row=i+1, pady=pady)