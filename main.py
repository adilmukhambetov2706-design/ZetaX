import customtkinter as ctk
import requests
from PIL import Image, ImageTk


API_KEY = "4bd17760355829f26b6a9130801ca914"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SkySphere Weather")
        self.geometry("900x600")

        self.configure(fg_color="#0a0b1e")

       
        self.header_label = ctk.CTkLabel(self, text="SkySphere", font=("Arial", 16, "bold"), text_color="white")
        self.header_label.pack(pady=10, padx=20, anchor="nw")

        self.title_label = ctk.CTkLabel(self, text="Discover the weather in\nevery city you go",
                                        font=("Arial", 32, "bold"), text_color="white")
        self.title_label.pack(pady=(40, 20))
