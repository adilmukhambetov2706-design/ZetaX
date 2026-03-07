from customtkinter import *
from PIL import Image
from random import randint

mb = 'Montserrat SemiBold'
m = 'Montserrat'
tr = 'transparent'

class Upper_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1293, height=40, fg_color=tr)
        color = "#D9D9D9"

        CTkLabel(self, text='Zeta-X', font=(mb, 32)).grid(column=0, row=0, padx=52)

        search_frame = CTkFrame(self, width=600, height=34, corner_radius=17, fg_color=color)
        search_frame.grid(column=1, row=0, padx=110)

        CTkLabel(search_frame, image=CTkImage(Image.open("Icons/Search.png"),
                                              size=(24, 24)), text="").grid(column=0, row=0, padx=(20, 0))

        search_entry = CTkEntry(search_frame, placeholder_text="Search", corner_radius=17, border_color=color,
                                fg_color=color, placeholder_text_color='#422BA0', width=671, height=34)
        search_entry.grid(column=1, row=0, padx=(0, 100))

        burger_image = CTkImage(light_image=Image.open('Icons/menu.png'), size=(58, 42))
        burger_button = CTkButton(self, image=burger_image, height=42, width=58, fg_color=tr,
                                  text="")
        burger_button.grid(column=2, row=0, padx=20)



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

        weather = ["Cloudy", "Lighting", "Wind", "Sun-clouds", "Rainning", "Sun-clouds", "Sun-ontheclouds", "Cloudy"]

        for i in range(6, 14):
            CTkLabel(hourly_time_frame, text=f"{i}:00", font=(mb, 32)).grid(column=i-6, row=0, padx=(0, 84))
        for i in range(8):
            weather_image = CTkImage(Image.open(f"Second/Weathers/{weather[i]}.png"), size=(80, 80))
            CTkLabel(hourly_time_frame, image=weather_image, text="").grid(column=i, row=1, padx=(0, 84), pady=(12, 0))
        for i in range(8):
            CTkLabel(hourly_time_frame, text="15°C", font=(m, 24)).grid(column=i, row=2, padx=(0, 84), pady=(12, 0))


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

        weekend = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weather = ["Cloudy", "Lighting", "Wind", "Sun-clouds", "Rainning", "Sun-clouds", "Sun-ontheclouds", "Cloudy"]
        name_weather = ["Cloudy", "Thunderstorm", "Sunny", "Rain", "Cloudy", "Cloudy"]
        pady=(1, 0)
        color = "#FFFFFF"

        for i in range(6):
            CTkLabel(self, text=weekend[i], text_color=color, font=font).grid(column=0, row=i + 1, pady=pady)
            CTkLabel(self, text=f"Mar {i}", text_color=color, font=font).grid(column=1, row=i + 1, pady=pady)

            weather_frame = CTkFrame(self, fg_color=tr)
            weather_frame.grid(column=2, row=i + 1, pady=pady)
            weather_image = CTkImage(Image.open(f"Second/Weathers/{weather[i]}.png"), size=(56, 56))
            CTkLabel(weather_frame, image=weather_image, text="").grid(column=0, row=0)
            CTkLabel(weather_frame, text=name_weather[i], text_color=color, font=font).grid(column=1, row=0)

            if i == 0:
                CTkLabel(self, text="14°/20°", text_color=color, font=font).grid(column=4, row=i+1, pady=pady)
            else:
                min_max_frame = CTkFrame(self, fg_color=tr)
                min_max_frame.grid(column=4, row=i + 1, pady=pady)
                CTkLabel(min_max_frame, text="14°", text_color="#0699D7", font=font).grid(column=0, row=0)
                CTkLabel(min_max_frame, text="/", text_color=color, font=font).grid(column=1, row=0)
                CTkLabel(min_max_frame, text="20°", text_color="#FF5A5A", font=font).grid(column=2, row=0)

            CTkLabel(self, text=str(randint(1, 15)), text_color=color, font=font).grid(column=5, row=i+1, pady=pady)
            CTkLabel(self, text=f"{str(randint(1, 15))}%", text_color=color, font=font).grid(column=6, row=i+1, pady=pady)