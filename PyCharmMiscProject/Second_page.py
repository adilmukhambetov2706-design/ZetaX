import threading
from customtkinter import *
from Frames import Upper_frame, Middle_frame, Lower_Frame, Additional_info_frame, Historical_day_frame
from NoInternetPage import NoInternetPage
from PIL import Image
from i18n import t

mb = 'Montserrat SemiBold'
m = 'Montserrat'
tr = 'transparent'


def clear_page(root):
    for child in root.winfo_children():
        child.destroy()


def show_no_internet_page(root, city="Bishkek", historical_date=None):
    root.city = city
    root.historical_date = historical_date
    root.geometry("900x600")
    root.title("No Internet")
    root.configure(bg="#12065A")

    def retry():
        build_second_page(root, city, historical_date)

    def open_settings():
        from Setting import SettingsPage

        settings_page = SettingsPage(root, city)
        settings_page.focus()

    page = NoInternetPage(root, retry, open_settings)
    page.pack(fill="both", expand=True)


def build_second_page(root, city="Bishkek", historical_date=None):
    root.city = city
    root.historical_date = historical_date
    root.geometry("1400x1252")
    root.title("ZetaX")
    root.configure(bg="#080451")
    clear_page(root)

    loading = CTkFrame(root, fg_color="#080451")
    loading.pack(fill="both", expand=True)
    CTkLabel(loading, text="Loading...", font=(m, 32), text_color="white").pack(expand=True)
    root.update_idletasks()

    def prefetch():
        try:
            from Weather_info import Mid_frame_info, Low_frame_info, Historical_day_info
            if historical_date:
                Historical_day_info(city, historical_date)
            else:
                Mid_frame_info(city)
                Low_frame_info(city)
            root.after(0, lambda: _build_ui(root, city, historical_date))
        except Exception:
            root.after(0, lambda: (clear_page(root), show_no_internet_page(root, city, historical_date)))

    threading.Thread(target=prefetch, daemon=True).start()


def _build_ui(root, city, historical_date):
    clear_page(root)
    try:
        upper_frame = Upper_frame(root)
        upper_frame.pack(anchor='n', pady=(23, 0))

        scroll_frame = CTkScrollableFrame(root, width=1400, height=1252, fg_color="#080451",
                                          corner_radius=59, border_color="#FFFFFF", border_width=1)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        kroshki_frame = CTkFrame(scroll_frame, fg_color=tr)
        kroshki_frame.pack(anchor='nw', padx=25)

        def go_home():
            from WeatherApp import WeatherApp
            root.destroy()
            WeatherApp().mainloop()

        CTkButton(kroshki_frame, text=t("home"), font=(mb, 14), fg_color="transparent",
                  hover_color="#1a1060", text_color="white", width=0, height=0,
                  command=go_home).grid(column=0, row=0)
        chevron_image = CTkImage(Image.open('Icons/chevron.png'), size=(24, 24))
        CTkLabel(kroshki_frame, image=chevron_image, text="").grid(column=1, row=0, padx=14)

        if historical_date:
            CTkButton(kroshki_frame, text=city, font=(mb, 14), fg_color="transparent",
                      hover_color="#1a1060", text_color="white", width=0, height=0,
                      command=lambda: build_second_page(root, city)).grid(column=2, row=0)
            CTkLabel(kroshki_frame, image=chevron_image, text="").grid(column=3, row=0, padx=14)
            CTkLabel(kroshki_frame, text=historical_date, font=(mb, 14)).grid(column=4, row=0)

            historical_frame = Historical_day_frame(scroll_frame, city, historical_date)
            historical_frame.pack(anchor='n', pady=(10, 0))
            historical_frame.pack_propagate(False)
        else:
            CTkLabel(kroshki_frame, text=city, font=(mb, 14)).grid(column=2, row=0)

            middle_frame = Middle_frame(scroll_frame, city)
            middle_frame.pack(anchor='n', pady=(10, 0))
            middle_frame.pack_propagate(False)

            add_info = Additional_info_frame(scroll_frame, city)
            add_info.pack(anchor='n', pady=(83, 0))
            add_info.pack_propagate(False)

            CTkLabel(scroll_frame, text='Extended 14-Day Outlook',
                     font=('Monteserrat', 48)).pack(anchor='n', pady=(57, 0))

            lower_frame = Lower_Frame(scroll_frame, city)
            lower_frame.pack(anchor='n', pady=(44, 0))
    except Exception:
        clear_page(root)
        show_no_internet_page(root, city, historical_date)


class Second(CTk):
    def __init__(self, city="Bishkek", historical_date=None):
        super().__init__()
        build_second_page(self, city, historical_date)


if __name__ == "__main__":
    a = Second()
    a.mainloop()
