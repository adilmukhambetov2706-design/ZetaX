import customtkinter as ctk


class LocationPermissionPage(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        allow_always_callback=None,
        allow_once_callback=None,
        close_callback=None
    ):
        super().__init__(parent, fg_color="#12065A")

        self.allow_always_callback = allow_always_callback
        self.allow_once_callback = allow_once_callback
        self.close_callback = close_callback

        self.create_widgets()

    def create_widgets(self):
        main_card = ctk.CTkFrame(
            self,
            fg_color="#160766",
            corner_radius=28
        )
        main_card.pack(fill="both", expand=True, padx=14, pady=14)

        close_btn = ctk.CTkButton(
            main_card,
            text="×",
            width=34,
            height=34,
            font=("Arial", 28),
            fg_color="transparent",
            hover_color="#2A1680",
            text_color="white",
            command=self.close
        )
        close_btn.place(relx=0.92, y=30, anchor="center")

        ctk.CTkLabel(
            main_card,
            text="ZETA-X requests",
            font=("Arial", 18),
            text_color="white"
        ).place(x=50, y=50)

        ctk.CTkLabel(
            main_card,
            text="permission for:",
            font=("Arial", 18),
            text_color="white"
        ).place(x=50, y=92)

        permission_row = ctk.CTkFrame(main_card, fg_color="transparent")
        permission_row.place(x=50, y=155)

        location_canvas = ctk.CTkCanvas(
            permission_row,
            width=42,
            height=58,
            bg="#160766",
            highlightthickness=0
        )
        location_canvas.pack(side="left", padx=(0, 18))

        location_canvas.create_oval(7, 4, 35, 34, outline="white", width=3)
        location_canvas.create_polygon(10, 26, 32, 26, 21, 56, fill="#160766", outline="white", width=3)
        location_canvas.create_oval(16, 14, 26, 24, fill="white", outline="white")

        text_block = ctk.CTkFrame(permission_row, fg_color="transparent")
        text_block.pack(side="left")

        ctk.CTkLabel(
            text_block,
            text="Access to your",
            font=("Arial", 15),
            text_color="white"
        ).pack(anchor="w", pady=(0, 14))

        ctk.CTkLabel(
            text_block,
            text="location data",
            font=("Arial", 15),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkButton(
            main_card,
            text="Allow while using the app",
            font=("Arial", 15, "bold"),
            width=480,
            height=66,
            corner_radius=33,
            fg_color="#3A1D91",
            hover_color="#4A2AA8",
            text_color="white",
            command=self.allow_always
        ).place(relx=0.5, y=292, anchor="center")

        ctk.CTkButton(
            main_card,
            text="Allow this time",
            font=("Arial", 15, "bold"),
            width=480,
            height=66,
            corner_radius=33,
            fg_color="#341987",
            hover_color="#4A2AA8",
            text_color="white",
            command=self.allow_once
        ).place(relx=0.5, y=392, anchor="center")

    def allow_always(self):
        if self.allow_always_callback:
            self.allow_always_callback()
        else:
            print("Location permission: while using the app")

    def allow_once(self):
        if self.allow_once_callback:
            self.allow_once_callback()
        else:
            print("Location permission: this time")

    def close(self):
        if self.close_callback:
            self.close_callback()
        else:
            self.pack_forget()


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("590x500")
    app.title("Location Permission")
    app.configure(fg_color="#bdbcc4")

    page = LocationPermissionPage(app)
    page.pack(fill="both", expand=True)

    app.mainloop()