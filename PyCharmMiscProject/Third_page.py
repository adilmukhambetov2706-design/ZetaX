from customtkinter import *
from PIL import Image
from Weather_info import Trd_page_info
from Frames import Upper_frame, get_saved_cities, save_city_to_db

m = 'Montserrat'
tr = 'transparent'
API_KEY = "d57a3845315ffcc38df8af6af61ffb9c"

class Lower_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=1344, height=407, fg_color="#1B166D", corner_radius=15)
        CTkLabel(self, text="My Saved Cities", font=(m, 48)).pack(anchor="n", pady=(20, 0))

        self.widgets_frames = CTkFrame(self, width=1242, height=287, fg_color=tr)
        self.widgets_frames.pack(anchor='n', pady=(30, 0))


class QuizApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x1252")
        self.title("ZetaX")
        self.city_column = 0
        self.displayed_cities = set()
        scroll_frame = CTkScrollableFrame(self, width=1400, height=1252, fg_color="#080451",
                                          corner_radius=59, border_color="#FFFFFF", border_width=1)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.upper_frame = Upper_frame(scroll_frame)
        self.upper_frame.pack(anchor='n', pady=(23, 0))
        self.upper_frame.add_city_button.configure(command=self.add_city_file)

        self.lower_frame = Lower_frame(scroll_frame)
        self.lower_frame.pack(anchor='n', pady=19)
        self.load_saved_cities()


    def add_city_file(self):
        city = self.upper_frame.search_entry.get().strip()
        if not city:
            return

        save_city_to_db(city, 1)
        self.show_city_card(city)

    def load_saved_cities(self):
        for city_number, city_name, saved_status in get_saved_cities():
            self.show_city_card(city_name)

    def show_city_card(self, city):
        city_key = city.lower()
        if city_key in self.displayed_cities:
            return

        font = CTkFont(family=m, size=32)
        padx = (35, 0)
        pady = (38, 0)

        third_page = Trd_page_info(city)
        self.displayed_cities.add(city_key)
        self.city_column += 1
        i = self.city_column - 1

        widget_frame = CTkFrame(self.lower_frame.widgets_frames, width=296, height=287, fg_color="#080451",
                                border_color="#FFFFFF", border_width=1)
        widget_frame.grid(column=i%4, row=i//4, padx=(0, 19), pady=(0, 19))

        CTkLabel(widget_frame, text=city, font=font).grid(column=0, row=0, padx=padx, pady=pady)

        image = Image.open(third_page.flag())
        flag_image = CTkImage(image, size=(60, 60))
        CTkLabel(widget_frame, image=flag_image, text="").grid(column=1, row=0, padx=(35, 37), pady=pady)

        CTkLabel(widget_frame, text=f"{int(third_page.temp())}°C", font=font).grid(column=0, row=1, padx=padx, pady=pady)

        pil_image = Image.open(third_page.icon()).resize((48, 48))
        mini_weather_image = CTkImage(pil_image, size=(48, 48))
        CTkLabel(widget_frame, image=mini_weather_image, text="").grid(column=1, row=1, padx=(35, 37), pady=pady)

        local_time = third_page.time()
        CTkLabel(widget_frame, text=local_time.strftime("%H:%M"), font=font).grid(column=0, row=2, padx=padx, pady=38)
        CTkLabel(widget_frame, text=third_page.country().upper(), font=font).grid(column=1, row=2, padx=(35, 37), pady=38)




if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
