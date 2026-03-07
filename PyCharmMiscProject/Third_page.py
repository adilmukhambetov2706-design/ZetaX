from customtkinter import *
from PIL import Image
from Frames import Upper_frame

class QuizApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x1252")
        self.title("ZetaX")
        scroll_frame = CTkScrollableFrame(self, width=1400, height=1252, fg_color="#080451",
                                          corner_radius=59, border_color="#FFFFFF", border_width=1)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        upper_frame = Upper_frame(scroll_frame)
        upper_frame.pack(anchor='n', pady=(23, 0))
        upper_frame.pack_propagate(False)

        lower_frame = CTkFrame(scroll_frame, width=1344, height=407, fg_color="#1B166D")
        lower_frame.pack(anchor='n', pady=19)

        CTkLabel(lower_frame, text="My Saved Cities", font=("Montserrat", 48)).pack(anchor="n", pady=(20, 0))

        widgets_frames = CTkFrame(lower_frame, width=1242, height=287, fg_color="transparent")
        widgets_frames.pack(anchor='n', pady=(30, 0), padx=51)

        flags = ["China", "France", "Japan", "Kazahstan"]
        mini_weather = ["sun", "cloud", "sun", "sun_clouds"]
        domen = ["CN", "FR", "JP", "KZ"]
        font = CTkFont(family="Montserrat", size=32)
        padx = (35, 0)
        pady = (38, 0)

        for i in range(4):
            widget_frame = CTkFrame(widgets_frames, width=296, height=287, fg_color="#080451",
                                    border_color="#FFFFFF", border_width=1)
            widget_frame.grid(column=i, row=0, padx=(0, 19))

            CTkLabel(widget_frame, text="BEIJING", font=font).grid(column=0, row=0, padx=padx, pady=pady)
            flag_image = CTkImage(Image.open(f"Third/Flags/{flags[i]}.png"), size=(60, 43))
            CTkLabel(widget_frame, image=flag_image, text="").grid(column=1, row=0, padx=(35, 37), pady=pady)

            CTkLabel(widget_frame, text="23°C", font=font).grid(column=0, row=1, padx=padx, pady=pady)
            mini_weather_image = flag_image = CTkImage(Image.open(
                f"Third/minimalistics_weather/minimalistic_{mini_weather[i]}.png"), size=(48, 48))
            CTkLabel(widget_frame, image=mini_weather_image, text="").grid(column=1, row=1, padx=(35, 37), pady=pady)

            CTkLabel(widget_frame, text="1:30 PM", font=font).grid(column=0, row=2, padx=padx, pady=(38, 38))
            CTkLabel(widget_frame, text=domen[i], font=font).grid(column=1, row=2, padx=(35, 37), pady=(38, 38))


app = QuizApp()
app.mainloop()