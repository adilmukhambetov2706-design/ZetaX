import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SettingsPage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("390x780")
        self.title("Settings")
        self.configure(fg_color="#050B45")

        self.selected_language = "Kyrgyz"

        self.build_ui()

    def build_ui(self):

        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#2D3AA8",
            scrollbar_button_hover_color="#3C4BCE"
        )
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        # =========================
        # HEADER
        # =========================

        top = ctk.CTkFrame(scroll, fg_color="transparent")
        top.pack(fill="x", pady=(5, 0))

        back_btn = ctk.CTkButton(
            top,
            text="←",
            width=34,
            height=34,
            corner_radius=17,
            fg_color="transparent",
            hover_color="#141D73",
            font=("Arial", 22)
        )
        back_btn.pack(anchor="w", padx=5)

        title = ctk.CTkLabel(
            scroll,
            text="Settings",
            font=("Arial", 38, "bold"),
            text_color="white"
        )
        title.pack(pady=(10, 0))

        subtitle = ctk.CTkLabel(
            scroll,
            text="Customize your weather experience",
            font=("Arial", 15),
            text_color="#8E95D9"
        )
        subtitle.pack(pady=(0, 30))

        # =========================
        # LANGUAGE
        # =========================

        self.section_title(scroll, "LANGUAGE")

        lang_card = self.card(scroll, 165)

        self.language_buttons = {}

        self.language_option(lang_card, "Kyrgyz")
        self.separator(lang_card)

        self.language_option(lang_card, "Russian")
        self.separator(lang_card)

        self.language_option(lang_card, "English")
        self.selected_language = "English"
        self.update_language_buttons()

        # =========================
        # THEME
        # =========================

        self.section_title(scroll, "THEME")

        theme_card = self.card(scroll, 110)

        self.option(theme_card, "Dark Theme", switch=True)
        self.separator(theme_card)

        self.option(theme_card, "Light Theme")

        # =========================
        # EXPORT DATA
        # =========================

        self.section_title(scroll, "EXPORT DATA")

        export_card = self.card(scroll, 190)

        top_row = ctk.CTkFrame(export_card, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(15, 8))

        export_label = ctk.CTkLabel(
            top_row,
            text="Export Excel",
            font=("Arial", 16),
            text_color="white"
        )
        export_label.pack(side="left")

        export_btn = ctk.CTkButton(
            top_row,
            text="Export",
            width=85,
            height=32,
            corner_radius=16,
            fg_color="#7D5CFF",
            hover_color="#6947F5",
            font=("Arial", 13, "bold")
        )
        export_btn.pack(side="right")

        export_weather = ctk.CTkLabel(
            export_card,
            text="Export Weather Data 📄",
            font=("Arial", 16),
            text_color="white"
        )
        export_weather.pack(anchor="w", padx=16, pady=(8, 0))

        desc = ctk.CTkLabel(
            export_card,
            text="Export weekly forecast\nExport air quality\nExport history",
            justify="left",
            font=("Arial", 12),
            text_color="#8E95D9"
        )
        desc.pack(anchor="w", padx=16, pady=(4, 0))

        open_btn = ctk.CTkButton(
            export_card,
            text="Open >",
            width=70,
            height=28,
            fg_color="transparent",
            hover_color="#1A247D",
            text_color="#8D6BFF",
            corner_radius=14,
            font=("Arial", 13, "bold")
        )
        open_btn.pack(anchor="e", padx=16, pady=(0, 12))

        # =========================
        # WEATHER HISTORY
        # =========================

        self.section_title(scroll, "WEATHER HISTORY")

        history_card = self.card(scroll, 145)

        hist_title = ctk.CTkLabel(
            history_card,
            text="Historical Archive",
            font=("Arial", 16),
            text_color="white"
        )
        hist_title.pack(anchor="w", padx=16, pady=(16, 0))

        hist_desc = ctk.CTkLabel(
            history_card,
            text="Access weather data from past years\nIncluding day and hourly records",
            justify="left",
            font=("Arial", 12),
            text_color="#8E95D9"
        )
        hist_desc.pack(anchor="w", padx=16, pady=(5, 0))

        view_btn = ctk.CTkButton(
            history_card,
            text="View >",
            width=70,
            height=28,
            fg_color="transparent",
            hover_color="#1A247D",
            text_color="#8D6BFF",
            corner_radius=14,
            font=("Arial", 13, "bold")
        )
        view_btn.pack(anchor="e", padx=16, pady=(5, 12))

    # =====================================
    # COMPONENTS
    # =====================================

    def section_title(self, parent, text):

        label = ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", 12),
            text_color="#8E95D9"
        )
        label.pack(anchor="w", padx=10, pady=(12, 8))

    def card(self, parent, height):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#18236D",
            corner_radius=24,
            height=height
        )
        frame.pack(fill="x", padx=6, pady=4)

        frame.pack_propagate(False)

        return frame

    def separator(self, parent):

        line = ctk.CTkFrame(
            parent,
            height=1,
            fg_color="#28358D"
        )
        line.pack(fill="x", padx=16)

    def option(self, parent, text, switch=False):

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=14)

        label = ctk.CTkLabel(
            row,
            text=text,
            font=("Arial", 16),
            text_color="white"
        )
        label.pack(side="left")

        if switch:
            sw = ctk.CTkSwitch(
                row,
                text="",
                progress_color="#7D5CFF",
                button_color="white",
                button_hover_color="#F2F2F2"
            )
            sw.select()
            sw.pack(side="right")

    # =====================================
    # LANGUAGE SWITCHING
    # =====================================

    def language_option(self, parent, text):

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=14)

        label = ctk.CTkLabel(
            row,
            text=text,
            font=("Arial", 16),
            text_color="white"
        )
        label.pack(side="left")

        switch = ctk.CTkSwitch(
            row,
            text="",
            progress_color="#7D5CFF",
            button_color="white",
            button_hover_color="#F2F2F2",
            command=lambda t=text: self.select_language(t)
        )
        switch.pack(side="right")

        self.language_buttons[text] = switch

    def select_language(self, language):

        self.selected_language = language
        self.update_language_buttons()

    def update_language_buttons(self):

        for lang, switch in self.language_buttons.items():

            if lang == self.selected_language:
                switch.select()
            else:
                switch.deselect()


if __name__ == "__main__":
    app = SettingsPage()
    app.mainloop()
