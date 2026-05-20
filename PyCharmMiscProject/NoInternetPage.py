import customtkinter as ctk
from PIL import Image


FONT = "Arial"


class NoInternetPage(ctk.CTkFrame):
    def __init__(self, parent, retry_callback=None, settings_callback=None):
        super().__init__(parent, fg_color="#09052d")
        self.retry_callback = retry_callback
        self.settings_callback = settings_callback
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Zeta-X",
            font=(FONT, 24, "bold"),
            text_color="white"
        ).place(x=40, y=24)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        cloud_image = ctk.CTkImage(Image.open("Second/Weathers/Clouds.png"), size=(120, 120))
        cloud_label = ctk.CTkLabel(center, image=cloud_image, text="")
        cloud_label.image = cloud_image
        cloud_label.pack(pady=(0, 16))
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
            command=self.retry,
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
            command=self.open_settings,
        ).pack(pady=8)

    def retry(self):
        if self.retry_callback:
            self.retry_callback()

    def open_settings(self):
        if self.settings_callback:
            self.settings_callback()
        else:
            print("Opening network settings...")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("900x600")
    app.title("No Internet")

    page = NoInternetPage(app)
    page.pack(fill="both", expand=True)

    app.mainloop()
