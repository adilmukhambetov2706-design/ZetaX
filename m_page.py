import os
from datetime import datetime, timezone, timedelta

import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageOps


FONT = "Arial"
API_KEY = os.getenv("OPENWEATHER_API_KEY", "372d1427a4f7c2495eb89f8e9ec537d1")


class NoInternetPage(ctk.CTkFrame):
    def __init__(self, parent, retry_callback):
        super().__init__(parent, fg_color="#09052d")
        self.retry_callback = retry_callback
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Zeta-X", font=(FONT, 24, "bold"), text_color="white").place(x=40, y=24)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center, text="☁️", font=(FONT, 78), text_color="white").pack(pady=(0, 16))
        ctk.CTkLabel(
            center,
            text="No internet connection",
            font=(FONT, 32, "bold"),
            text_color="white",
        ).pack(pady=(0, 34))

        ctk.CTkButton(
            center,
            text="Repeat",
            font=(FONT, 16, "bold"),
            width=250,
            height=44,
            corner_radius=22,
            fg_color="#372397",
            hover_color="#4630b8",
            command=self.retry_callback,
        ).pack(pady=8)

        ctk.CTkButton(
            center,
            text="Check settings",
            font=(FONT, 16),
            width=280,
            height=44,
            corner_radius=22,
            fg_color="#1b145d",
            hover_color="#261d76",
            command=lambda: print("Opening network settings..."),
        ).pack(pady=8)


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Zeta-X Weather")
        self.geometry("1000x650")
        self.minsize(900, 600)
        self.configure(fg_color="#2b1688")

        self.search_dropdown = None
        self.is_error_showing = False
        self.main_photo = self.load_photo()

        self.create_widgets()
        self.error_page = NoInternetPage(self, retry_callback=self.check_connection_again)
        self.after(500, self.start_network_monitoring)

    def create_widgets(self):
        self.shell = ctk.CTkFrame(
            self,
            fg_color="#090239",
            border_width=1,
            border_color="#d8d3ff",
            corner_radius=36,
        )
        self.shell.pack(fill="both", expand=True, padx=66, pady=28)
        self.shell.pack_propagate(False)

        self.header = ctk.CTkFrame(self.shell, fg_color="transparent")
        self.header.pack(fill="x", padx=28, pady=(14, 4))

        ctk.CTkLabel(self.header, text="Zeta-X", font=(FONT, 21, "bold"), text_color="white").pack(side="left")

        self.search_container = ctk.CTkFrame(self.header, fg_color="#5435a3", corner_radius=12)
        self.search_container.pack(side="left", padx=(150, 0))

        ctk.CTkLabel(self.search_container, text="⌕", font=(FONT, 12), text_color="white").pack(side="left", padx=(10, 2))
        self.search_entry = ctk.CTkEntry(
            self.search_container,
            placeholder_text="Search",
            width=360,
            height=22,
            corner_radius=11,
            fg_color="#e7e7ef",
            text_color="#17132f",
            placeholder_text_color="#68637e",
            border_width=0,
        )
        self.search_entry.pack(side="left", padx=(0, 0))
        self.search_entry.bind("<KeyRelease>", self.on_search_type)

        ctk.CTkLabel(self.header, text="☰", font=(FONT, 28), text_color="#d8d3ff").pack(side="right")

        self.top_panel = ctk.CTkFrame(
            self.shell,
            fg_color="#080231",
            border_width=1,
            border_color="#d8d3ff",
            corner_radius=18,
        )
        self.top_panel.pack(fill="x", padx=18, pady=(4, 16), ipady=16)

        ctk.CTkLabel(
            self.top_panel,
            text="Discover the weather in every city you go",
            font=(FONT, 31, "bold"),
            text_color="white",
        ).pack(pady=(22, 24))

        cards = ctk.CTkFrame(self.top_panel, fg_color="transparent")
        cards.pack(fill="x", padx=88)

        self.left_icon_label, self.left_temp_label = self.weather_card(cards, "#2d128d", "☀️", "16", "Yesterday", False)
        self.icon_label, self.temp_label = self.weather_card(cards, "#4a3299", "☁️", "-3", "Bishkek, Kyrgyzstan", True)
        self.right_icon_label, self.right_temp_label = self.weather_card(cards, "#2d128d", "🌤️", "9", "Tomorrow", False)

        bottom = ctk.CTkFrame(
            self.shell,
            fg_color="#1d0a71",
            border_width=1,
            border_color="#d8d3ff",
            corner_radius=14,
        )
        bottom.pack(fill="both", expand=True, padx=14, pady=(0, 18))
        bottom.grid_columnconfigure(1, weight=1)
        bottom.grid_rowconfigure(0, weight=1)

        self.create_weather_details(bottom)
        self.create_photo_card(bottom)
        self.create_air_quality(bottom)

        self.bind("<Button-1>", self.close_dropdown)
        self.image_card.bind("<Configure>", self.set_fitted_image)

    def weather_card(self, parent, color, icon, temp, label, is_main):
        card = ctk.CTkFrame(
            parent,
            fg_color=color,
            border_width=1,
            border_color="#d8d3ff",
            corner_radius=18,
            width=176,
            height=196,
        )
        card.pack(side="left", expand=True, padx=24)
        card.pack_propagate(False)

        icon_label = ctk.CTkLabel(card, text=icon, font=(FONT, 28), text_color="white")
        icon_label.pack(pady=(24, 0))

        temp_row = ctk.CTkFrame(card, fg_color="transparent")
        temp_row.pack(pady=(12, 0))
        temp_label = ctk.CTkLabel(temp_row, text=temp, font=(FONT, 52 if is_main else 50), text_color="white")
        temp_label.pack(side="left")
        ctk.CTkLabel(temp_row, text="°C", font=(FONT, 12), text_color="#d8d3ff").pack(side="left", anchor="n", pady=12)

        text_color = "#d8d3ff" if is_main else "white"
        city = ctk.CTkLabel(card, text=label, font=(FONT, 14), text_color=text_color)
        city.pack(pady=(8, 0))
        if is_main:
            self.city_label = city
        return icon_label, temp_label

    def create_weather_details(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color="#130e5f",
            border_width=1,
            border_color="#d8d3ff",
            corner_radius=9,
            width=250,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(18, 8), pady=10)
        card.grid_propagate(False)
        card.grid_columnconfigure((0, 1), weight=1)

        wind_box = ctk.CTkFrame(card, fg_color="#1a126b", border_width=1, border_color="#d8d3ff", corner_radius=7)
        wind_box.grid(row=0, column=0, padx=(14, 6), pady=(12, 8), sticky="nsew")
        ctk.CTkLabel(wind_box, text="༄ WIND", font=(FONT, 9, "bold"), text_color="#765aa8").pack(pady=(8, 3))
        self.wind_label = ctk.CTkLabel(wind_box, text="9.7\nKM/H", font=(FONT, 15, "bold"), text_color="white")
        self.wind_label.pack()

        sun_box = ctk.CTkFrame(card, fg_color="#1a126b", border_width=1, border_color="#d8d3ff", corner_radius=7)
        sun_box.grid(row=0, column=1, padx=(6, 14), pady=(28, 8), sticky="nsew")
        ctk.CTkLabel(sun_box, text="♨ SUNRISE", font=(FONT, 9, "bold"), text_color="#765aa8").pack(pady=(10, 4))
        self.sunrise_time_label = ctk.CTkLabel(sun_box, text="6:05 AM", font=(FONT, 15), text_color="white")
        self.sunrise_time_label.pack()
        ctk.CTkLabel(sun_box, text="Sunset: 6:56 PM", font=(FONT, 7), text_color="#d8d3ff").pack(pady=(10, 0))

        ctk.CTkLabel(
            card,
            text="ⓘ Stay informed",
            font=(FONT, 9),
            text_color="white",
            fg_color="#322085",
            corner_radius=8,
            width=110,
            height=18,
        ).grid(row=1, column=0, columnspan=2, pady=(0, 8))

        ctk.CTkLabel(
            card,
            text="Get complete weather\ninformation every day",
            font=(FONT, 14, "bold"),
            text_color="white",
            justify="left",
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=22)

    def create_photo_card(self, parent):
        self.image_card = ctk.CTkFrame(parent, fg_color="#050416", border_width=1, border_color="#d8d3ff", corner_radius=8)
        self.image_card.grid(row=0, column=1, sticky="nsew", padx=8, pady=10)
        self.image_label = ctk.CTkLabel(self.image_card, text="")
        self.image_label.pack(fill="both", expand=True)

    def create_air_quality(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color="#130e5f",
            border_width=1,
            border_color="#d8d3ff",
            corner_radius=9,
            width=210,
        )
        card.grid(row=0, column=2, sticky="nsew", padx=(8, 18), pady=10)
        card.grid_propagate(False)

        meter = ctk.CTkFrame(card, fg_color="#1a126b", border_width=1, border_color="#d8d3ff", corner_radius=7)
        meter.pack(fill="x", padx=14, pady=(12, 12))

        ctk.CTkLabel(meter, text="▤ AIR QUALITY", font=(FONT, 8, "bold"), text_color="#765aa8").pack(anchor="w", padx=12, pady=(8, 3))
        self.aqi_status_label = ctk.CTkLabel(meter, text="3-Low Health Risk", font=(FONT, 12, "bold"), text_color="white")
        self.aqi_status_label.pack(anchor="w", padx=12)

        self.air_line_frame = ctk.CTkFrame(meter, width=150, height=20, fg_color="transparent")
        self.air_line_frame.pack(anchor="w", padx=12, pady=(4, 0))
        ctk.CTkFrame(self.air_line_frame, width=150, height=3, fg_color="#e44ad9", corner_radius=2).place(x=0, y=4)
        self.chevron_label = ctk.CTkLabel(self.air_line_frame, text="⌃", font=(FONT, 12), text_color="#ff76f1")
        self.chevron_label.place(x=65, y=6)

        more = ctk.CTkFrame(meter, fg_color="transparent")
        more.pack(fill="x", padx=12, pady=(0, 8))
        ctk.CTkLabel(more, text="See more", font=(FONT, 8, "bold"), text_color="white").pack(side="left")
        ctk.CTkLabel(more, text="›", font=(FONT, 14), text_color="#d65bef").pack(side="right")

        ctk.CTkLabel(
            card,
            text="♡ Take care of your health",
            font=(FONT, 8, "bold"),
            text_color="white",
            fg_color="#332985",
            corner_radius=9,
            width=128,
            height=18,
        ).pack(anchor="w", padx=18, pady=(6, 16))

        ctk.CTkLabel(
            card,
            text="Get information on air\nquality",
            font=(FONT, 13, "bold"),
            text_color="white",
            justify="left",
        ).pack(anchor="w", padx=18)

    def start_network_monitoring(self):
        if self.has_connection():
            if self.is_error_showing:
                self.error_page.pack_forget()
                self.is_error_showing = False
        elif not self.is_error_showing:
            self.close_dropdown()
            self.error_page.pack(fill="both", expand=True)
            self.error_page.lift()
            self.is_error_showing = True

        self.after(5000, self.start_network_monitoring)

    def check_connection_again(self):
        if self.has_connection():
            self.error_page.pack_forget()
            self.is_error_showing = False
        else:
            print("Подключение всё еще отсутствует...")

    def has_connection(self):
        try:
            requests.get("https://www.google.com/generate_204", timeout=2)
            return True
        except requests.RequestException:
            return False

    def on_search_type(self, event):
        if self.is_error_showing:
            return

        query = self.search_entry.get().strip()
        if not query:
            self.close_dropdown()
            return

        if self.search_dropdown is None:
            self.search_dropdown = ctk.CTkFrame(
                self.shell,
                width=400,
                height=96,
                fg_color="#1e1e4a",
                corner_radius=14,
                border_width=1,
                border_color="#7560d8",
            )

        x_pos = self.search_container.winfo_x()
        y_pos = self.search_container.winfo_y() + self.search_container.winfo_height() + 8
        self.search_dropdown.place(x=x_pos, y=y_pos)
        self.search_dropdown.lift()

        for widget in self.search_dropdown.winfo_children():
            widget.destroy()

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": query, "appid": API_KEY, "units": "metric"},
                timeout=2,
            )
            if response.status_code == 200:
                data = response.json()
                city_name = data.get("name", query)
                country = data.get("sys", {}).get("country", "")
                temp = round(data.get("main", {}).get("temp", 0))
                text = f"⌕  {city_name}, {country} ({temp}°C)"

                ctk.CTkButton(
                    self.search_dropdown,
                    text=text,
                    font=(FONT, 14),
                    fg_color="transparent",
                    hover_color="#30308a",
                    anchor="w",
                    command=lambda name=city_name: self.select_city(name),
                ).pack(fill="x", padx=10, pady=14, ipady=9)
            else:
                ctk.CTkLabel(
                    self.search_dropdown,
                    text="Nothing found...",
                    font=(FONT, 14, "italic"),
                    text_color="#b6b0d8",
                ).pack(expand=True)
        except requests.RequestException:
            ctk.CTkLabel(
                self.search_dropdown,
                text="Connection error",
                font=(FONT, 14, "italic"),
                text_color="#b6b0d8",
            ).pack(expand=True)

    def select_city(self, city_name):
        try:
            current = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city_name, "appid": API_KEY, "units": "metric"},
                timeout=3,
            )
            forecast = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={"q": city_name, "appid": API_KEY, "units": "metric"},
                timeout=3,
            )
            if current.status_code != 200 or forecast.status_code != 200:
                return

            current_data = current.json()
            forecast_data = forecast.json()
            self.update_current_weather(current_data)
            self.update_air_quality(current_data)
            self.update_forecast(forecast_data)
        except Exception as exc:
            print(f"Ошибка обновления данных погоды: {exc}")
        finally:
            self.search_entry.delete(0, "end")
            self.close_dropdown()

    def update_current_weather(self, data):
        sys_data = data.get("sys", {})
        temp = round(data.get("main", {}).get("temp", 0))
        wind = data.get("wind", {}).get("speed", 0)
        weather_main = data.get("weather", [{}])[0].get("main", "")

        self.city_label.configure(text=f"{data.get('name', '')}, {sys_data.get('country', '')}")
        self.temp_label.configure(text=str(temp))
        self.wind_label.configure(text=f"{round(wind * 3.6, 1)}\nKM/H")
        self.icon_label.configure(text=self.get_weather_emoji(weather_main, temp))

        sunrise_ts = sys_data.get("sunrise")
        timezone_offset = data.get("timezone", 0)
        if sunrise_ts:
            local_sunrise = datetime.fromtimestamp(sunrise_ts, tz=timezone.utc) + timedelta(seconds=timezone_offset)
            self.sunrise_time_label.configure(text=local_sunrise.strftime("%-I:%M %p" if os.name != "nt" else "%#I:%M %p"))

    def update_air_quality(self, data):
        coord = data.get("coord", {})
        if "lat" not in coord or "lon" not in coord:
            return

        aqi_val = 3
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/air_pollution",
                params={"lat": coord["lat"], "lon": coord["lon"], "appid": API_KEY},
                timeout=2,
            )
            aqi_val = response.json()["list"][0]["main"]["aqi"]
        except Exception:
            pass

        aqi_names = {
            1: "1-Good",
            2: "2-Fair",
            3: "3-Moderate",
            4: "4-Poor",
            5: "5-Very Poor",
        }
        self.aqi_status_label.configure(text=aqi_names.get(aqi_val, "Unknown"))
        self.chevron_label.place_configure(x=12 + (aqi_val - 1) * 31)

    def update_forecast(self, data):
        forecast_list = data.get("list", [])
        if len(forecast_list) > 16:
            tomorrow = forecast_list[8]
            after_tomorrow = forecast_list[16]

            tomorrow_temp = round(tomorrow.get("main", {}).get("temp", 0))
            tomorrow_main = tomorrow.get("weather", [{}])[0].get("main", "")
            self.right_temp_label.configure(text=str(tomorrow_temp))
            self.right_icon_label.configure(text=self.get_weather_emoji(tomorrow_main, tomorrow_temp))

            after_temp = round(after_tomorrow.get("main", {}).get("temp", 0))
            after_main = after_tomorrow.get("weather", [{}])[0].get("main", "")
            self.left_temp_label.configure(text=str(after_temp))
            self.left_icon_label.configure(text=self.get_weather_emoji(after_main, after_temp))

    def get_weather_emoji(self, main_state, temp):
        main_state = main_state.lower()
        if "cloud" in main_state:
            return "☁️"
        if "rain" in main_state or "drizzle" in main_state:
            return "🌧️"
        if "snow" in main_state:
            return "❄️"
        if "thunder" in main_state:
            return "⛈️"
        return "🌙" if temp < 5 else "☀️"

    def close_dropdown(self, event=None):
        if self.search_dropdown and event is not None:
            if event.widget in (self.search_entry, self.search_container):
                return
        if self.search_dropdown:
            self.search_dropdown.destroy()
            self.search_dropdown = None

    def load_photo(self):
        for file_name in ("download.jpg", "download.png", "city.jpg", "city.png"):
            if os.path.exists(file_name):
                return Image.open(file_name).convert("RGBA")

        width, height = 900, 360
        image = Image.new("RGBA", (width, height), "#050817")
        draw = ImageDraw.Draw(image)
        for y in range(height):
            blue = int(20 + y * 0.18)
            draw.line((0, y, width, y), fill=(4, 10, blue, 255))
        for x in range(0, width, 42):
            building_h = 70 + (x * 31) % 130
            draw.rectangle((x, height - building_h, x + 28, height), fill=(8, 16, 35, 255))
            for yy in range(height - building_h + 12, height - 10, 22):
                if (x + yy) % 3 == 0:
                    draw.rectangle((x + 8, yy, x + 12, yy + 4), fill=(255, 201, 92, 210))
        draw.line((width // 2 - 30, height, width // 2 + 20, height // 2), fill=(230, 220, 210, 130), width=5)
        draw.line((width // 2 + 34, height, width // 2 + 68, height // 2), fill=(255, 117, 84, 150), width=4)
        return image.filter(ImageFilter.GaussianBlur(0.2))

    def set_fitted_image(self, event=None):
        width = event.width if event else self.image_card.winfo_width()
        height = event.height if event else self.image_card.winfo_height()
        if width < 10 or height < 10:
            return

        fitted = ImageOps.fit(self.main_photo, (width, height), centering=(0.5, 0.5))
        mask = Image.new("L", (width, height), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, width, height), radius=8, fill=255)
        rounded = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        rounded.paste(fitted, (0, 0), mask=mask)

        ctk_image = ctk.CTkImage(light_image=rounded, dark_image=rounded, size=(width, height))
        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
