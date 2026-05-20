import customtkinter as ctk
import calendar
from datetime import datetime

ctk.set_appearance_mode("dark")

MONTHS = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
]

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class CalendarWidget(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#08112B")

        self.selected_date = None

        now = datetime.now()

        self.current_year = now.year
        self.current_month = now.month

        self.min_year = now.year - 5
        self.max_year = now.year

        self.build_ui()
        self.draw_calendar()

    def build_ui(self):

        title = ctk.CTkLabel(self, text="Calendar", font=("Arial", 34, "bold"))
        title.pack(anchor="nw", padx=25, pady=(20, 10))

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=15)

        self.prev_month_btn = ctk.CTkButton(top_frame, text="<", width=40, command=self.prev_month)
        self.prev_month_btn.grid(row=0, column=0, padx=5)

        self.month_label = ctk.CTkLabel(top_frame, text="", width=140, font=("Arial", 20, "bold"))
        self.month_label.grid(row=0, column=1, padx=10)

        self.next_month_btn = ctk.CTkButton(top_frame, text=">", width=40, command=self.next_month)
        self.next_month_btn.grid(row=0, column=2, padx=5)

        self.prev_year_btn = ctk.CTkButton(top_frame, text="<<", width=50, command=self.prev_year)
        self.prev_year_btn.grid(row=0, column=3, padx=(30, 5))

        self.year_label = ctk.CTkLabel(top_frame, text="", width=90, font=("Arial", 20, "bold"))
        self.year_label.grid(row=0, column=4, padx=5)

        self.next_year_btn = ctk.CTkButton(top_frame, text=">>", width=50, command=self.next_year)
        self.next_year_btn.grid(row=0, column=5, padx=5)

        self.calendar_frame = ctk.CTkFrame(self, fg_color="#1B2742", corner_radius=25)
        self.calendar_frame.pack(padx=20, pady=20)

        self.select_button = ctk.CTkButton(self, text="Select Date", height=55, corner_radius=25,
                                           font=("Arial", 24, "bold"), fg_color="#7C3AED", hover_color="#6D28D9", command=self.print_date)
        self.select_button.pack(side="bottom", fill="x", padx=40, pady=30)

    def draw_calendar(self):

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.configure(text=MONTHS[self.current_month - 1])

        self.year_label.configure(text=str(self.current_year))

        for i, day in enumerate(DAYS):

            lbl = ctk.CTkLabel(self.calendar_frame, text=day, text_color="#9FA9C0", font=("Arial", 15, "bold"))
            lbl.grid(row=0, column=i, padx=12, pady=15)

        month_days = calendar.monthcalendar(self.current_year, self.current_month)

        today = datetime.now()

        for row, week in enumerate(month_days, start=1):

            for col, day in enumerate(week):

                if day == 0:
                    continue

                is_future = (
                    self.current_year > today.year
                    or (
                        self.current_year == today.year
                        and self.current_month > today.month
                    )
                    or (
                        self.current_year == today.year
                        and self.current_month == today.month
                        and day > today.day
                    )
                )

                state = "disabled" if is_future else "normal"

                btn = ctk.CTkButton(self.calendar_frame, text=str(day), width=42, height=42, corner_radius=21,
                                    fg_color="#2563EB", hover_color="#1D4ED8", state=state,
                                    command=lambda d=day: self.select_date(d))
                btn.grid(row=row, column=col, padx=6, pady=8)

    def select_date(self, day):

        self.selected_date = (
            f"{day:02d}."
            f"{self.current_month:02d}."
            f"{self.current_year}"
        )

        self.select_button.configure(
            text=self.selected_date
        )

    def print_date(self):

        print(self.selected_date)

    def prev_month(self):

        self.current_month -= 1

        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        if self.current_year < self.min_year:
            self.current_year = self.min_year
            self.current_month = 1

        self.draw_calendar()

    def next_month(self):

        now = datetime.now()

        self.current_month += 1

        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1

        if (
            self.current_year > now.year
            or (
                self.current_year == now.year
                and self.current_month > now.month
            )
        ):
            self.current_year = now.year
            self.current_month = now.month

        self.draw_calendar()

    def prev_year(self):

        if self.current_year > self.min_year:
            self.current_year -= 1

        self.draw_calendar()

    def next_year(self):

        now = datetime.now()

        if self.current_year < now.year:
            self.current_year += 1

        if self.current_year == now.year:
            if self.current_month > now.month:
                self.current_month = now.month

        self.draw_calendar()


app = ctk.CTk()
app.geometry("500x700")
app.configure(fg_color="#08112B")

calendar_widget = CalendarWidget(app)
calendar_widget.pack(fill="both", expand=True)

app.mainloop()