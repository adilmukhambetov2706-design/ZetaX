from customtkinter import *
from PIL import Image
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from Weather_info import Mid_frame_info, Low_frame_info

mb = 'Montserrat SemiBold'
m = 'Montserrat'
tr = 'transparent'
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

DB_PATH = Path(__file__).with_name("cities.db")


def create_cities_table():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cities (
                city_number INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL UNIQUE,
                saved_status INTEGER NOT NULL CHECK(saved_status IN (1, 2))
            )
            """
        )


def save_city_to_db(city_name, saved_status=1):
    create_cities_table()
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO cities (city_name, saved_status)
            VALUES (?, ?)
            ON CONFLICT(city_name) DO UPDATE SET saved_status = excluded.saved_status
            """,
            (city_name, saved_status),
        )
        cursor.execute(
            "SELECT city_number, city_name, saved_status FROM cities WHERE city_name = ?",
            (city_name,),
        )
        return cursor.fetchone()


def get_saved_cities():
    create_cities_table()
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT city_number, city_name, saved_status
            FROM cities
            WHERE saved_status = 1
            ORDER BY city_number
            """
        )
        return cursor.fetchall()

class Upper_frame(CTkFrame):
    def __init__(self, master):
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

        self.add_city_button = CTkButton(self, text="Add city", height=34, fg_color="#1B166D", corner_radius=17,
                                    border_color="white", border_width=1, width=60, font=(m, 16),
                                    command=self.add_city)
        self.add_city_button.grid(column=2, row=0, padx=10)

        burger_image = CTkImage(light_image=Image.open('Icons/menu.png'), size=(58, 42))
        self.burger_button = CTkButton(self, image=burger_image, height=42, width=58, fg_color=tr,
                                  text="", command=self.open_menu)
        self.burger_button.grid(column=3, row=0, padx=60)


    def add_city(self):
        city = self.search_entry.get().strip()
        if not city:
            return
        city_data = save_city_to_db(city, 1)
        print(city_data)

    def open_menu(self):
        root = self.winfo_toplevel()
        root.update_idletasks()

        overlay = CTkToplevel(root)
        overlay.overrideredirect(True)
        overlay.transient(root)
        overlay.configure(fg_color="#080451")
        overlay.attributes("-alpha", 0.79)

        width = root.winfo_width()
        height = root.winfo_height()
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        overlay.geometry(f"{width}x{height}+{x}+{y}")

        menu_frame = CTkFrame(overlay, width=420, height=520, fg_color="#01003E")
        menu_frame.place(relx=0.64, y=105)
        menu_frame.pack_propagate(False)

        button_style = {
            "width": 360,
            "height": 54,
            "corner_radius": 24,
            "fg_color": "#53517F",
            "hover_color": "#646299",
            "text_color": "white",
            "anchor": "w",
            "font": (mb, 24),
        }

        CTkButton(menu_frame, text="Saved Cities", **button_style).pack(anchor="n", pady=32)
        CTkButton(menu_frame, text="Notifications", **button_style).pack(anchor="n")
        CTkButton(menu_frame, text="Settings", command=lambda: self.open_settings_page(overlay), **button_style).pack(anchor="n", pady=32)

        overlay.bind("<Escape>", lambda event: overlay.destroy())
        overlay.bind("<Button-1>", lambda event: overlay.destroy() if event.widget == overlay else None)
        overlay.focus_force()

    def open_settings_page(self, overlay):
        from Setting import SettingsPage

        root = self.winfo_toplevel()
        overlay.destroy()
        root.destroy()

        settings_page = SettingsPage()
        settings_page.mainloop()


class Middle_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1344, height=605, fg_color="#161358",
                         corner_radius=15, border_color="white", border_width=1)
        mid_frame = Mid_frame_info()

        CTkLabel(self, text='Bishkek: Detailed 14-Day & Hourly Forecast',
                 font=(m, 48)).pack(anchor='n', pady=(33, 0))

        detailed_24h_frame = CTkFrame(self, fg_color=tr, width=1292, height=365, corner_radius=15)
        detailed_24h_frame.pack(anchor='n', pady=(42, 0), padx=(1, 1))
        detailed_24h_frame.pack_propagate(False)

        CTkLabel(detailed_24h_frame, text='Bishkek: Detailed (24 Hours)',
                  font=(mb, 24)).pack(anchor='n', pady=(15, 0))

        hourly_time_frame = CTkScrollableFrame(detailed_24h_frame, width=1180, height=235,
                                               fg_color=tr, orientation="horizontal")
        hourly_time_frame.pack(anchor="n", pady=(20, 0), padx=(39, 0))
        local_time = mid_frame.time_right_now()
        for i in range(24):
            hour_time = local_time + timedelta(hours=i)
            CTkLabel(hourly_time_frame, text=f"{hour_time.hour:02d}:00", font=(mb, 32)).grid(column=i, row=0, padx=(0, 84))

            weather = mid_frame.weather_today(i//3)
            weather_image = CTkImage(Image.open(f"Second/Weathers/{weather}.png"), size=(80, 80))
            CTkLabel(hourly_time_frame, image=weather_image, text="").grid(column=i, row=1, padx=(0, 84), pady=(12, 0))

            city_temp = mid_frame.temp_today(i//3)
            CTkLabel(hourly_time_frame, text=f"{int(city_temp)}°C", font=(m, 24)).grid(column=i, row=2, padx=(0, 84), pady=(12, 0))



class Additional_info_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1344, height=360, fg_color="#080451")
        color = "#0D0C4C"
        mid_frame = Mid_frame_info()

        main_frame = CTkFrame(self, width=925, height=354, fg_color="#130F60",
                              border_width=1, border_color="white", corner_radius=15)
        main_frame.grid(column=0, row=0)

        wind_frame = CTkFrame(main_frame, width=231, height=196, fg_color=color,
                              border_width=1, border_color="white", corner_radius=8)
        wind_frame.grid(column=0, row=0, pady=(25, 0), padx=(26, 0))
        wind_frame.pack_propagate(False)
        mini_wind_frame = CTkFrame(wind_frame, fg_color=color)
        mini_wind_frame.pack(anchor="n", pady=(10, 0))
        wind_image = CTkImage(Image.open("Icons/Wind.png"), size=(17, 17))
        CTkLabel(mini_wind_frame, image=wind_image, text="").grid(column=0, row=0)
        CTkLabel(mini_wind_frame, text="WIND", text_color="#7E4FB2", font=(mb, 18)).grid(column=1, row=0, padx=(8, 0))

        wind_side_frame = CTkFrame(wind_frame, width=153, height=151, fg_color=color)
        wind_side_frame.pack(anchor="n", pady=(3, 0))
        wind_side_frame.pack_propagate(False)

        wind_direction = mid_frame.wind_direction_degrees()
        wind_side_pil = Image.open("Icons/Wind_side.png").rotate(-wind_direction, resample=Image.Resampling.BICUBIC)
        wind_side_image = CTkImage(wind_side_pil, size=(153, 151))
        CTkLabel(wind_side_frame, image=wind_side_image, text="").place(x=0, y=0)

        CTkLabel(wind_side_frame, text="N", fg_color=color, font=(mb, 14)).place(relx=0.5, y=31, anchor="center")
        CTkLabel(wind_side_frame, text="E", fg_color=color, font=(mb, 14)).place(x=113, rely=0.5, anchor="center")
        CTkLabel(wind_side_frame, text="S", fg_color=color, font=(mb, 14)).place(relx=0.5, y=115, anchor="center")
        CTkLabel(wind_side_frame, text="W", fg_color=color, font=(mb, 14)).place(x=40, rely=0.5, anchor="center")

        CTkLabel(wind_side_frame, text=f"{mid_frame.wind_speed():.1f}", fg_color=color, font=(m, 30)).place(relx=0.5, rely=0.44, anchor="center")
        CTkLabel(wind_side_frame, text="KM/H", fg_color=color, font=(m, 15)).place(relx=0.5, rely=0.6, anchor="center")


        sunrise_frame = CTkFrame(main_frame, width=231, height=196, fg_color=color,
                              border_width=1, border_color="white", corner_radius=8)
        sunrise_frame.grid(column=1, row=0, pady=(25, 16), padx=87)
        mini_sunrise_frame = CTkFrame(sunrise_frame, fg_color=color)
        mini_sunrise_frame.pack(anchor="n", pady=23)
        sunrise_image = CTkImage(Image.open("Icons/sun-rise.png"), size=(17, 17))
        CTkLabel(mini_sunrise_frame, image=sunrise_image, text="").grid(column=0, row=0)
        CTkLabel(mini_sunrise_frame, text="SUNRISE", text_color="#5F3D95", font=(mb, 14)).grid(column=1, row=0)
        CTkLabel(sunrise_frame, text=mid_frame.sunrise_time(), font=(m, 24)).pack(anchor='n')
        sunrise_image = CTkImage(Image.open("Icons/sun-rise_time.png"), size=(228, 44))
        CTkLabel(sunrise_frame, image=sunrise_image, text="").pack(anchor='n', pady=(13, 44))
        

        sunset_frame = CTkFrame(main_frame, width=231, height=196, fg_color=color,
                              border_width=1, border_color="white", corner_radius=8)
        sunset_frame.grid(column=2, row=0, pady=(25, 0), padx=(0, 26))
        mini_sunset_frame = CTkFrame(sunset_frame, fg_color=color)
        mini_sunset_frame.pack(anchor="n", pady=23)
        sunset_image = CTkImage(Image.open("Icons/sun-set.png"), size=(17, 17))
        CTkLabel(mini_sunset_frame, image=sunset_image, text="").grid(column=0, row=0)
        CTkLabel(mini_sunset_frame, text="SUNSET", text_color="#5F3D95", font=(mb, 14)).grid(column=1, row=0)
        CTkLabel(sunset_frame, text=mid_frame.sunset_time(), font=(m, 24)).pack(anchor='n')
        sunset_image = CTkImage(Image.open("Icons/sun-set-time.png"), size=(228, 44))
        CTkLabel(sunset_frame, image=sunset_image, text="").pack(anchor='n', pady=(13, 44))


        informed_frame = CTkFrame(main_frame, width=231, height=32, fg_color="#35327E",
                                  border_width=1, border_color="white", corner_radius=13)
        informed_frame.grid(column=1, row=1)
        alert_image = CTkImage(Image.open("Icons/alert.png"), size=(21, 21))
        CTkLabel(informed_frame, image=alert_image, text="").grid(column=0, row=0, padx=(31, 2))
        CTkLabel(informed_frame, text="Stay informed", font=(mb, 20)).grid(column=1, row=0, padx=(0, 31))

        CTkLabel(main_frame, text="Get complete weather information every day", font=(mb, 20)).grid(column=1, row=2, pady=23)


        air_quality_frame = CTkFrame(self, fg_color="#130F60", width=293, height=287,
                                     border_width=1, border_color="white", corner_radius=15)
        air_quality_frame.grid(column=1, row=0, padx=25, pady=38)

        mini_air_quality_frame = CTkFrame(air_quality_frame, fg_color="#1B1854", width=263,
                                          height=165, border_width=1, border_color="white", corner_radius=8)
        mini_air_quality_frame.pack(anchor="n", pady=(15, 18), padx=15)
        mini_air_quality_frame.pack_propagate(False)

        air_header_frame = CTkFrame(mini_air_quality_frame, fg_color="#1B1854")
        air_header_frame.pack(anchor="w", padx=20, pady=(14, 10))
        air_image = CTkImage(Image.open("Icons/Air.png"), size=(18, 18))
        CTkLabel(air_header_frame, image=air_image, text="").grid(column=0, row=0)
        CTkLabel(air_header_frame, text="AIR QUALITY", text_color="#A262D7", font=(mb, 10)).grid(column=1, row=0, padx=(8, 0))

        CTkLabel(mini_air_quality_frame, text="3-Low Health Risk", font=(mb, 16),
                 text_color="white").pack(anchor="w", padx=20)

        air_line_frame = CTkFrame(mini_air_quality_frame, width=228, height=38, fg_color="#1B1854")
        air_line_frame.pack(anchor="w", padx=20, pady=(5, 0))
        air_line_frame.pack_propagate(False)

        air_line_image = CTkImage(Image.open("Icons/line.png"), size=(228, 4))
        CTkLabel(air_line_frame, image=air_line_image, text="", fg_color="#1B1854").pack(anchor="w")

        chevron_pil = Image.open("Icons/chevron.png").rotate(90, expand=True)
        chevron_image = CTkImage(chevron_pil, size=(34, 24))
        air_quality = mid_frame.air_quality()
        CTkLabel(air_line_frame, image=chevron_image, text="", fg_color="#1B1854").pack(anchor="w", padx=(10+air_quality*36, 0), pady=(4, 0))

        see_more_frame = CTkFrame(mini_air_quality_frame, fg_color="#1B1854")
        see_more_frame.pack(anchor="w", fill="x", padx=20, pady=(2, 0))
        CTkLabel(see_more_frame, text="See more", font=(mb, 12),  text_color="white").grid(column=0, row=0, sticky="w")
        CTkLabel(see_more_frame, text=">", font=(m, 12), text_color="#B95FD6").grid(column=1, row=0, sticky="e")
        see_more_frame.grid_columnconfigure(1, weight=1)


        care_frame = CTkFrame(air_quality_frame, fg_color="#35327E", width=161, height=26,
                              border_width=1, border_color="white", corner_radius=13)
        care_frame.pack(anchor="n", padx=15)
        heart_image = CTkImage(Image.open("Icons/Heart.png"), size=(12, 12))
        CTkLabel(care_frame, image=heart_image, text="").grid(column=0, row=0, padx=8)
        CTkLabel(care_frame, text="Take care of your health", font=(mb, 10)).grid(column=1, row=0, padx=(0, 8))

        CTkLabel(air_quality_frame, text="Get information on air", font=(mb, 20)).pack(anchor="n", pady=(15, 5), padx=15)
        CTkLabel(air_quality_frame, text="quality", font=(mb, 20)).pack(anchor="n", pady=(0, 18), padx=15)






class Lower_Frame(CTkFrame):
    def __init__(self, master):
        low_frame = Low_frame_info()
        font = CTkFont(m, 24)
        font_semibold = CTkFont(mb, 28)
        pady=(30, 0)
        color = "#B8B7CF"
        super().__init__(master, width=1344, height=431, fg_color="#130F60", corner_radius=15,
                         border_color="white", border_width=1)

        CTkLabel(self, text='Day', text_color=color, font=font_semibold).grid(column=0, row=0, padx=(21, 0), pady=pady)
        CTkLabel(self, text='Date', text_color=color, font=font_semibold).grid(column=1, row=0, padx=(76, 0), pady=pady)
        CTkLabel(self, text='Weather', text_color=color, font=font_semibold).grid(column=2, row=0, padx=(80, 0), pady=pady)
        CTkLabel(self, text='', width=207).grid(column=3, row=0,pady=pady)
        CTkLabel(self, text='Min / Max', text_color=color, font=font_semibold).grid(column=4, row=0, pady=pady)
        CTkLabel(self, text='UV Index', text_color=color, font=font_semibold).grid(column=5, row=0, padx=(78, 0), pady=pady)
        CTkLabel(self, text='Humidity', text_color=color, font=font_semibold).grid(column=6, row=0, padx=(81, 23), pady=pady)

        pady=(1, 0)
        color = "#FFFFFF"

        for i in range(min(13, low_frame.days_count())):
            today = datetime.now()
            day = today + timedelta(days=i)
            CTkLabel(self, text=day.strftime("%a"), text_color=color, font=font).grid(column=0, row=i+1, pady=pady)

            date = low_frame.date(i)
            CTkLabel(self, text=f"{months[date.month-1]} {date.day}",
                     text_color=color, font=font).grid(column=1, row=i+1, pady=pady)

            weather_frame = CTkFrame(self, fg_color=tr)
            weather_frame.grid(column=2, row=i+1, pady=pady)

            weather = low_frame.weather_today(i)
            weather_image = CTkImage(Image.open(f"Second/Weathers/{weather}.png"), size=(56, 56))
            CTkLabel(weather_frame, image=weather_image, text="").grid(column=0, row=0)
            CTkLabel(weather_frame, text=weather, text_color=color, font=font).grid(column=1, row=0)

            min_temp = int(low_frame.min_temp(i))
            max_temp = int(low_frame.max_temp(i))
            if i == 0:
                CTkLabel(self, text=f"{min_temp}°/{max_temp}°", text_color=color, font=font).grid(column=4, row=i+1, pady=pady)
            else:
                min_max_frame = CTkFrame(self, fg_color=tr)
                min_max_frame.grid(column=4, row=i+1, pady=pady)
                CTkLabel(min_max_frame, text=f"{min_temp}°", text_color="#0699D7", font=font).grid(column=0, row=0)
                CTkLabel(min_max_frame, text="/", text_color=color, font=font).grid(column=1, row=0)
                CTkLabel(min_max_frame, text=f"{max_temp}°", text_color="#FF5A5A", font=font).grid(column=2, row=0)


            CTkLabel(self, text=f"{low_frame.UV_day(i):.1f}", text_color=color, font=font).grid(column=5, row=i+1, pady=pady)

            humidity = int(low_frame.humidity(i))
            CTkLabel(self, text=f"{humidity}%", text_color=color, font=font).grid(column=6, row=i+1, pady=pady)
