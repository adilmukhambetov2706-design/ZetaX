import os

import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from NoInternetPage import NoInternetPage
from Weather_info import Mid_frame_info
from Frames import SunriseCard, AirQualityCard, WindSideCard, Upper_frame


FONT = "Arial"


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Zeta-X Weather")
        self.geometry("1400x955")
        self.resizable(False, False)
        self.configure(fg_color="#4A2BA0")

        self.city = "Bishkek"
        self.main_photo = self.load_photo()
        self.is_error_showing = False
        self.error_page = None
        self.monitor_after_id = None

        self.show_main_page()
        self.monitor_after_id = self.after(500, self.start_network_monitoring)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def clear_page(self):
        for child in self.winfo_children():
            child.destroy()

    def show_main_page(self):
        self.clear_page()
        self.is_error_showing = False
        self.create_widgets()
        self.error_page = NoInternetPage(self, retry_callback=self.check_connection_again)

    def show_no_internet_page(self):
        self.clear_page()
        self.error_page = NoInternetPage(self, retry_callback=self.check_connection_again)
        self.error_page.pack(fill="both", expand=True)
        self.is_error_showing = True

    def create_widgets(self):
        shell = ctk.CTkFrame(
            self,
            width=1290,
            height=895,
            fg_color="#080451",
            corner_radius=36,
            border_width=1,
            border_color="#FFFFFF",
        )
        shell.place(x=55, y=38)
        shell.pack_propagate(False)

        self.upper_frame = Upper_frame(shell)
        self.upper_frame.place(x=0, y=20)
        self.upper_frame.add_city_button.configure(command=self.open_selected_city)

        top_panel = ctk.CTkFrame(
            shell,
            width=1238,
            height=465,
            fg_color="#110750",
            corner_radius=20,
            border_width=1,
            border_color="#FFFFFF",
        )
        top_panel.place(x=26, y=92)

        ctk.CTkLabel(
            top_panel,
            text="Discover the weather in every city you go",
            font=(FONT, 45, "bold"),
            text_color="white",
        ).place(relx=0.5, y=88, anchor="center")

        self.weather_card(top_panel, 150, "#2d128d", "Clear", "16", "Yesterday", False)
        self.weather_card(top_panel, 510, "#4a3299", "Clouds", "-3", "Bishkek, Kyrgyzstan", True)
        self.weather_card(top_panel, 870, "#2d128d", "Clouds", "9", "Tomorrow", False)

        self.create_bottom_panel(shell)
        self.bind_open_third_page(shell)

    def weather_card(self, parent, x, color, weather, temp, label, is_main):
        card = ctk.CTkFrame(
            parent,
            width=260,
            height=292,
            fg_color=color,
            corner_radius=22,
            border_width=1,
            border_color="#d8d3ff",
        )
        card.place(x=x, y=150)
        card.pack_propagate(False)

        icon_name = "Clouds" if weather == "Clouds" else "Clear"
        icon = ctk.CTkImage(Image.open(f"Second/Weathers/{icon_name}.png"), size=(72, 72))
        icon_label = ctk.CTkLabel(card, image=icon, text="")
        icon_label.image = icon
        icon_label.pack(pady=(38, 0))

        temp_row = ctk.CTkFrame(card, fg_color="transparent")
        temp_row.pack(pady=(22, 0))
        ctk.CTkLabel(temp_row, text=temp, font=(FONT, 84 if is_main else 80), text_color="white").pack(side="left")
        ctk.CTkLabel(temp_row, text="°C", font=(FONT, 22), text_color="#d8d3ff").pack(side="left", anchor="n", pady=18)

        text_color = "#d8d3ff" if is_main else "white"
        ctk.CTkLabel(card, text=label, font=(FONT, 22), text_color=text_color).pack(pady=(2, 0))

    def create_bottom_panel(self, parent):
        bottom = ctk.CTkFrame(
            parent,
            width=1240,
            height=315,
            fg_color="#1d0a71",
            corner_radius=20,
            border_width=1,
            border_color="#FFFFFF",
        )
        bottom.place(x=25, y=580)

        try:
            info = Mid_frame_info(self.city)
        except Exception:
            info = None

        left = ctk.CTkFrame(bottom, width=520, height=285, fg_color="#130F60",
                            border_width=1, border_color="#FFFFFF", corner_radius=12)
        left.place(x=18, y=20)

        if info:
            wind_frame = WindSideCard(left, info)
            wind_frame.place(x=20, y=26)

            sunrise_frame = SunriseCard(left, info)
            sunrise_frame.place(x=270, y=26)
        else:
            self.mini_metric(left, 20, 26, "WIND", "9.7\nKM/H")
            self.mini_metric(left, 270, 26, "SUNRISE", "6:05 AM")

        ctk.CTkLabel(left, text="Stay informed", font=(FONT, 14), text_color="white",
                     fg_color="#35327E", corner_radius=13, width=150, height=28).place(x=92, y=226)
        ctk.CTkLabel(left, text="Get complete weather\ninformation every day",
                     font=(FONT, 17, "bold"), text_color="white", justify="left").place(x=20, y=242)

        self.create_photo_card(bottom)
        if info:
            air_quality_frame = AirQualityCard(bottom, info)
            air_quality_frame.place(x=930, y=14)
        else:
            self.create_air_quality_card(bottom, 3)
        self.image_card.bind("<Configure>", self.set_fitted_image)

    def bind_open_third_page(self, widget):
        widget.bind("<Button-1>", self.open_third_page)
        for child in widget.winfo_children():
            if child in (self.upper_frame.search_entry, self.upper_frame.add_city_button, self.upper_frame.burger_button):
                continue
            self.bind_open_third_page(child)

    def open_third_page(self, event=None):
        if event and event.widget in (self.upper_frame.search_entry, self.upper_frame.add_city_button, self.upper_frame.burger_button):
            return

        from Third_page import QuizApp

        if self.monitor_after_id:
            self.after_cancel(self.monitor_after_id)
            self.monitor_after_id = None
        self.destroy()
        third_page = QuizApp()
        third_page.mainloop()

    def mini_metric(self, parent, x, y, title, value):
        box = ctk.CTkFrame(parent, width=166, height=142, fg_color="#1B1854",
                           border_width=1, border_color="#FFFFFF", corner_radius=10)
        box.place(x=x, y=y)
        ctk.CTkLabel(box, text=title, font=(FONT, 14, "bold"), text_color="#765aa8").pack(pady=(16, 5))
        ctk.CTkLabel(box, text=value, font=(FONT, 24), text_color="white").pack()

    def create_photo_card(self, parent):
        self.image_card = ctk.CTkFrame(
            parent,
            width=340,
            height=285,
            fg_color="#050416",
            corner_radius=12,
            border_width=1,
            border_color="#FFFFFF",
        )
        self.image_card.place(x=560, y=15)
        self.image_label = ctk.CTkLabel(self.image_card, text="")
        self.image_label.pack(fill="both", expand=True)

    def create_air_quality_card(self, parent, aqi):
        card = ctk.CTkFrame(parent, width=265, height=245, fg_color="#130F60",
                            border_width=1, border_color="#FFFFFF", corner_radius=12)
        card.place(x=945, y=20)

        meter = ctk.CTkFrame(card, width=225, height=112, fg_color="#1B1854",
                             border_width=1, border_color="#FFFFFF", corner_radius=9)
        meter.place(x=20, y=18)
        ctk.CTkLabel(meter, text="AIR QUALITY", font=(FONT, 12, "bold"), text_color="#765aa8").place(x=16, y=10)
        ctk.CTkLabel(meter, text=f"{aqi}-Low Health Risk", font=(FONT, 16, "bold"), text_color="white").place(x=16, y=36)
        ctk.CTkFrame(meter, width=180, height=4, fg_color="#e44ad9").place(x=16, y=70)
        ctk.CTkLabel(meter, text="See more >", font=(FONT, 12), text_color="white").place(x=16, y=82)

        ctk.CTkLabel(card, text="Take care of your health", font=(FONT, 12), text_color="white",
                     fg_color="#35327E", corner_radius=13, width=180, height=28).place(x=20, y=150)
        ctk.CTkLabel(card, text="Get information on air\nquality",
                     font=(FONT, 20, "bold"), text_color="white", justify="left").place(x=20, y=190)

    def open_selected_city(self):
        from Second_page import build_second_page

        city = self.upper_frame.search_entry.get().strip()
        if city:
            build_second_page(self, city)

    def start_network_monitoring(self):
        if self.has_connection():
            if self.is_error_showing:
                self.show_main_page()
        elif not self.is_error_showing:
            self.show_no_internet_page()

        self.monitor_after_id = self.after(5000, self.start_network_monitoring)

    def close_app(self):
        if self.monitor_after_id:
            self.after_cancel(self.monitor_after_id)
            self.monitor_after_id = None
        self.destroy()

    def check_connection_again(self):
        if self.has_connection():
            self.show_main_page()
        else:
            print("Connection is still unavailable...")

    def has_connection(self):
        try:
            requests.get("https://www.google.com/generate_204", timeout=2)
            return True
        except requests.RequestException:
            return False

    def load_photo(self):
        for file_name in ("Second/download.png", "Second/download.jpg", "download.jpg", "download.png", "city.jpg", "city.png"):
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
