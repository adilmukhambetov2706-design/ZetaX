import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Zeta-X Weather")
        self.geometry("1000x650")
        ctk.set_appearance_mode("dark")


        self.configure(fg_color="#0a0a2e")

        self.create_widgets()

    def create_widgets(self):
        # --- 1. Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=20)

        ctk.CTkLabel(header_frame, text="Zeta-X", font=("Arial", 24, "bold")).pack(side="left")

        search_entry = ctk.CTkEntry(header_frame, placeholder_text="Search", width=400,
                                    corner_radius=20, fg_color="#1e1e4a", border_width=0)
        search_entry.pack(side="left", padx=50)

        ctk.CTkLabel(header_frame, text="≡", font=("Arial", 30)).pack(side="right")

        # --- 2. Main Banner ---
        banner_card = ctk.CTkFrame(self, fg_color="#16164d", corner_radius=30, border_width=1, border_color="#3d3d8e")
        banner_card.pack(fill="x", padx=40, pady=10, ipady=40)

        ctk.CTkLabel(banner_card, text="Discover the weather in every city you go",
                     font=("Arial", 32, "bold")).pack(pady=(20, 30))

        temp_container = ctk.CTkFrame(banner_card, fg_color="transparent")
        temp_container.pack()

        ctk.CTkLabel(temp_container, text="☀️ 16°C", font=("Arial", 22)).pack(side="left", padx=20)

        main_temp_box = ctk.CTkFrame(temp_container, fg_color="#30308a", corner_radius=20, width=200, height=180)
        main_temp_box.pack_propagate(False)
        main_temp_box.pack(side="left", padx=20)

        ctk.CTkLabel(main_temp_box, text="🌙", font=("Arial", 40)).pack(pady=(20, 0))
        ctk.CTkLabel(main_temp_box, text="-3°", font=("Arial", 60, "bold")).pack()
        ctk.CTkLabel(main_temp_box, text="Bishkek, Kyrgyzstan", font=("Arial", 14)).pack()

        ctk.CTkLabel(temp_container, text="🌤️ 9°C", font=("Arial", 22)).pack(side="left", padx=20)

        # --- 3. Bottom Grid ---

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="both", expand=True, padx=40, pady=20)


        info_card = ctk.CTkFrame(self.bottom_frame, fg_color="#16164d", corner_radius=20, width=280)
        info_card.pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(info_card, text="༄ WIND: 9.7 KM/H", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(info_card, text="🌅 SUNRISE: 6:05 AM", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(info_card, text="Stay informed\nGet complete weather info",
                     font=("Arial", 12), text_color="gray").pack(side="bottom", pady=20)


        self.image_card = ctk.CTkFrame(self.bottom_frame, fg_color="#000", corner_radius=20)
        self.image_card.pack(side="left", fill="both", expand=True, padx=10)

        self.image_label = ctk.CTkLabel(self.image_card, text="")
        self.image_label.pack(expand=True, fill="both")


        self.aqi_card = ctk.CTkFrame(self.bottom_frame, fg_color="#16164d", corner_radius=20, width=280)
        self.aqi_card.pack(side="left", fill="y", padx=(10, 0))
        self.aqi_card.pack_propagate(False)

        ctk.CTkLabel(self.aqi_card, text="AIR QUALITY", font=("Arial", 12, "bold"), text_color="#aaa").pack(
            pady=(20, 5))
        ctk.CTkLabel(self.aqi_card, text="3-Low Health Risk", font=("Arial", 16, "bold")).pack()

        self.progress = ctk.CTkProgressBar(self.aqi_card, width=200, height=8, progress_color="#ff4dff",
                                           fg_color="#3d3d8e")
        self.progress.set(0.3)
        self.progress.pack(pady=20)

        ctk.CTkLabel(self.aqi_card, text="Take care of your health\nGet info on air quality",
                     font=("Arial", 12), text_color="gray").pack(side="bottom", pady=20)


        self.after(100, self.set_fitted_image)

    def set_fitted_image(self):
        try:

            img = Image.open("download.jpg")
            width = self.image_card.winfo_width()
            height = self.image_card.winfo_height()

            if width > 10 and height > 10:
                img_fitted = ImageOps.fit(img, (width, height), centering=(0.5, 0.5))
                ctk_img = ctk.CTkImage(light_image=img_fitted, dark_image=img_fitted, size=(width, height))
                self.image_label.configure(image=ctk_img)
                self.image_label.image = ctk_img
        except Exception as e:
            self.image_label.configure(text="Добавьте city.jpg в папку")


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()