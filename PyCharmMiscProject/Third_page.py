import threading
from concurrent.futures import ThreadPoolExecutor
from customtkinter import *
from PIL import Image

from Frames import Upper_frame, get_saved_cities, save_city_to_db
from NoInternetPage import NoInternetPage
from Weather_info import Trd_page_info
from i18n import t


m = "Montserrat"
tr = "transparent"

_city_loader = ThreadPoolExecutor(max_workers=16)


def _city_name(city: str) -> str:
    key = city.lower().strip()
    translated = t(key)
    if translated != key:
        return translated.title()
    return city.strip().title()


class Lower_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1344, height=720, fg_color="#1B166D", corner_radius=15)
        CTkLabel(self, text=t("savedCities"), font=(m, 48)).pack(anchor="n", pady=(20, 0))

        self.widgets_frames = CTkFrame(self, width=1242, height=610, fg_color=tr)
        self.widgets_frames.pack(anchor="n", pady=(30, 0))


class QuizApp(CTk):
    def __init__(self):
        super().__init__()
        self.build_page()

    def clear_page(self):
        for child in self.winfo_children():
            child.destroy()

    def show_no_internet_page(self):
        self.clear_page()
        self.geometry("900x600")
        self.title("No Internet")
        self.configure(bg="#12065A")

        def open_settings():
            from Setting import SettingsPage

            settings_page = SettingsPage(self, getattr(self, "city", "Bishkek"))
            settings_page.focus()

        page = NoInternetPage(self, self.build_page, open_settings)
        page.pack(fill="both", expand=True)

    def build_page(self):
        self.clear_page()
        self.geometry("1400x1252")
        self.title("ZetaX")
        self.city_column = 0
        self.displayed_cities = set()

        scroll_frame = CTkScrollableFrame(
            self,
            width=1400,
            height=1252,
            fg_color="#080451",
            corner_radius=59,
            border_color="#FFFFFF",
            border_width=1,
        )
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.upper_frame = Upper_frame(scroll_frame)
        self.upper_frame.pack(anchor="n", pady=(23, 0))
        self.upper_frame.add_city_button.configure(command=self.add_city_file)

        self.lower_frame = Lower_frame(scroll_frame)
        self.lower_frame.pack(anchor="n", pady=19)
        self.after(100, self.safe_load_saved_cities)

    def safe_load_saved_cities(self):
        try:
            self.load_saved_cities()
        except Exception:
            self.show_no_internet_page()

    def add_city_file(self):
        city = self.upper_frame.search_entry.get().strip()
        if not city:
            return
        save_city_to_db(city, 1)
        self.show_city_card_safe(city)

    def load_saved_cities(self):
        for city_number, city_name, saved_status in get_saved_cities():
            self.show_city_card_safe(city_name)

    def show_city_card_safe(self, city):
        try:
            self.show_city_card(city)
        except Exception:
            self.show_city_card(city, use_fallback=True)

    def open_second_page(self, city):
        from Second_page import build_second_page

        build_second_page(self, city)

    def bind_city_card_click(self, widget, city):
        if getattr(widget, "is_delete_button", False):
            return
        widget.bind("<Button-1>", lambda event, selected_city=city: self.open_second_page(selected_city))
        widget.configure(cursor="hand2")
        for child in widget.winfo_children():
            self.bind_city_card_click(child, city)

    def delete_city(self, city):
        save_city_to_db(city, 2)
        self.build_page()

    def show_city_card(self, city, use_fallback=False):
        city_key = city.lower()
        if city_key in self.displayed_cities:
            return

        font = CTkFont(family=m, size=32)
        padx = (35, 0)
        pady = (38, 0)

        self.displayed_cities.add(city_key)
        self.city_column += 1
        i = self.city_column - 1

        widget_frame = CTkFrame(
            self.lower_frame.widgets_frames,
            width=296,
            height=287,
            fg_color="#080451",
            border_color="#FFFFFF",
            border_width=1,
        )
        widget_frame.grid(column=i % 4, row=i // 4, padx=(0, 36), pady=(0, 36))

        delete_button = CTkButton(
            widget_frame,
            text="X",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="#2A1B7A",
            hover_color="#5C2FB8",
            border_width=1,
            border_color="#FFFFFF",
            font=(m, 15, "bold"),
            command=lambda selected_city=city: self.delete_city(selected_city),
        )
        delete_button.is_delete_button = True
        delete_button.place(relx=1, x=-10, y=10, anchor="ne")

        placeholder = CTkImage(Image.open("Second/Weathers/Clouds.png"), size=(60, 60))

        city_label = CTkLabel(widget_frame, text=_city_name(city), font=font)
        city_label.grid(column=0, row=0, padx=padx, pady=pady)

        flag_label = CTkLabel(widget_frame, image=placeholder, text="")
        flag_label.grid(column=1, row=0, padx=(35, 37), pady=pady)

        temp_label = CTkLabel(widget_frame, text="--°C", font=font)
        temp_label.grid(column=0, row=1, padx=padx, pady=pady)

        weather_label = CTkLabel(widget_frame, image=placeholder, text="")
        weather_label.grid(column=1, row=1, padx=(35, 37), pady=pady)

        time_label = CTkLabel(widget_frame, text="--:--", font=font)
        time_label.grid(column=0, row=2, padx=padx, pady=38)

        country_label = CTkLabel(widget_frame, text="--", font=font)
        country_label.grid(column=1, row=2, padx=(35, 37), pady=38)

        self.bind_city_card_click(widget_frame, city)

        if not use_fallback:
            _city_loader.submit(
                self._load_city_data,
                city, widget_frame, temp_label, flag_label, weather_label, time_label, country_label,
            )

    def _load_city_data(self, city, widget_frame, temp_label, flag_label, weather_label, time_label, country_label):
        try:
            info = Trd_page_info(city)

            flag_bytes = [None]
            icon_bytes = [None]

            def fetch_flag():
                flag_bytes[0] = info.flag()

            def fetch_icon():
                icon_bytes[0] = info.icon()

            t_flag = threading.Thread(target=fetch_flag, daemon=True)
            t_icon = threading.Thread(target=fetch_icon, daemon=True)
            t_flag.start()
            t_icon.start()
            t_flag.join()
            t_icon.join()

            if flag_bytes[0] is None or icon_bytes[0] is None:
                return

            temp_text = f"{int(info.temp())}°C"
            local_time_text = info.time().strftime("%H:%M")
            country_text = info.country().upper()
            flag_img = CTkImage(Image.open(flag_bytes[0]), size=(60, 60))
            weather_img = CTkImage(Image.open(icon_bytes[0]).resize((48, 48)), size=(48, 48))

            def update():
                if not widget_frame.winfo_exists():
                    return
                temp_label.configure(text=temp_text)
                flag_label.configure(image=flag_img)
                flag_label.image = flag_img
                weather_label.configure(image=weather_img)
                weather_label.image = weather_img
                time_label.configure(text=local_time_text)
                country_label.configure(text=country_text)

            self.after(0, update)
        except Exception:
            pass


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
