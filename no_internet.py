import customtkinter as ctk


class NoInternetPage(ctk.CTkFrame):
    def __init__(self, parent, retry_callback=None, settings_callback=None):
        super().__init__(parent, fg_color="#12065A")

        self.retry_callback = retry_callback
        self.settings_callback = settings_callback

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Zeta-X",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).place(x=40, y=25)

        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.52, anchor="center")

        cloud_canvas = ctk.CTkCanvas(
            center_frame,
            width=120,
            height=90,
            bg="#12065A",
            highlightthickness=0
        )
        cloud_canvas.pack(pady=(0, 15))

        cloud_canvas.create_oval(28, 38, 68, 78, fill="#1FA8FF", outline="")
        cloud_canvas.create_oval(48, 22, 92, 76, fill="#4BBEFF", outline="")
        cloud_canvas.create_oval(70, 42, 108, 76, fill="#2AA7F2", outline="")
        cloud_canvas.create_rectangle(34, 52, 100, 76, fill="#209FF0", outline="")
        cloud_canvas.create_line(38, 10, 86, 82, fill="#E6E6F2", width=3)

        ctk.CTkLabel(
            center_frame,
            text="No internet connection",
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=(0, 32))

        ctk.CTkButton(
            center_frame,
            text="repeat",
            font=("Arial", 17, "bold"),
            width=230,
            height=42,
            corner_radius=22,
            fg_color="#4C4997",
            hover_color="#5A57AD",
            text_color="white",
            command=self.retry
        ).pack(pady=(0, 16))

        ctk.CTkButton(
            center_frame,
            text="check settings",
            font=("Arial", 17, "bold"),
            width=300,
            height=42,
            corner_radius=22,
            fg_color="#4C4997",
            hover_color="#5A57AD",
            text_color="white",
            command=self.open_settings
        ).pack()

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