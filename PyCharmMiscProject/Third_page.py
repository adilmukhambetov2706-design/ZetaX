from customtkinter import *
from PIL import Image
import requests
from Frames import Upper_frame
from io import BytesIO
from datetime import datetime, timedelta

m = 'Montserrat'
tr = 'transparent'
API_KEY = "d57a3845315ffcc38df8af6af61ffb9c"

class Lower_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1344, height=407, fg_color="#1B166D", corner_radius=15)
        CTkLabel(self, text="My Saved Cities", font=(m, 48)).pack(anchor="n", pady=(20, 0))

        self.widgets_frames = CTkFrame(self, width=1242, height=287, fg_color=tr)
        self.widgets_frames.pack(anchor='n', pady=(30, 0), padx=51)


class QuizApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x1252")
        self.title("ZetaX")
        self.city_column = 0
        scroll_frame = CTkScrollableFrame(self, width=1400, height=1252, fg_color="#080451",
                                          corner_radius=59, border_color="#FFFFFF", border_width=1)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.upper_frame = Upper_frame(scroll_frame, n=3)
        self.upper_frame.pack(anchor='n', pady=(23, 0))

        add_city_button = CTkButton(self.upper_frame, text="Add city", height=34, fg_color="#1B166D", corner_radius=17,
                                    border_color="#FFFFFF", border_width=1, width=60, font=(m, 16), command=self.add_city)
        add_city_button.grid(column=2, row=0, padx=10)


        self.lower_frame = Lower_frame(scroll_frame)
        self.lower_frame.pack(anchor='n', pady=19)


    def add_city(self):
        font = CTkFont(family=m, size=32)
        padx = (35, 0)
        pady = (38, 0)

        self.city_column += 1
        i = self.city_column - 1
        city = str(self.upper_frame.search_entry.get())

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
        weather_data = requests.get(url).json()
        city_temp = weather_data['list'][0]['main']['temp']

        response = requests.get(
            f"https://nominatim.openstreetmap.org/search?city={city}&format=json&addressdetails=1",
            headers={"User-Agent": "my-app"}).json()
        country_code = response[0]["address"]["country_code"]

        response = requests.get(f"https://flagsapi.com/{country_code.upper()}/flat/64.png")
        img_data = BytesIO(response.content)
        image = Image.open(img_data)

        icon_code = weather_data['list'][0]['weather'][0]['icon']
        response = requests.get(f"https://openweathermap.org/img/wn/{icon_code}@2x.png")
        pil_image = Image.open(BytesIO(response.content)).resize((48, 48))

        timezone_offset = weather_data['city']['timezone']
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(seconds=timezone_offset)



        widget_frame = CTkFrame(self.lower_frame.widgets_frames, width=296, height=287, fg_color="#080451",
                                border_color="#FFFFFF", border_width=1)
        widget_frame.grid(column=i%4, row=i//4, padx=(0, 19), pady=(0, 19))

        CTkLabel(widget_frame, text=city, font=font).grid(column=0, row=0, padx=padx, pady=pady)

        flag_image = CTkImage(image, size=(60, 60))
        CTkLabel(widget_frame, image=flag_image, text="").grid(column=1, row=0, padx=(35, 37), pady=pady)

        CTkLabel(widget_frame, text=f"{int(city_temp)}°C", font=font).grid(column=0, row=1, padx=padx, pady=pady)

        mini_weather_image = CTkImage(pil_image, size=(48, 48))
        CTkLabel(widget_frame, image=mini_weather_image, text="").grid(column=1, row=1, padx=(35, 37), pady=pady)

        CTkLabel(widget_frame, text=local_time.strftime("%H:%M"), font=font).grid(column=0, row=2, padx=padx, pady=38)
        CTkLabel(widget_frame, text=country_code.upper(), font=font).grid(column=1, row=2, padx=(35, 37), pady=38)




app = QuizApp()
app.mainloop()