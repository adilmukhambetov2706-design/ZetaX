from customtkinter import *
from PIL import Image
from First_stage import Upper_frame, Middle_frame, Lower_Frame

class Second(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1400x1252")
        self.title("ZetaX")
        scroll_frame = CTkScrollableFrame(self, width=1400, height=1252, fg_color="#080451", corner_radius=59)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        upper_frame = Upper_frame(scroll_frame)
        upper_frame.pack(anchor='n', pady=(23, 0))
        upper_frame.pack_propagate(False)

        middle_frame = Middle_frame(scroll_frame)
        middle_frame.pack(anchor='n', pady=(19, 0))
        middle_frame.pack_propagate(False)

        CTkLabel(scroll_frame, text='Extended 14-Day Outlook',
                 font=('Monteserrat', 48)).pack(anchor='n', pady=(57, 0))

        lower_frame = Lower_Frame(scroll_frame)
        lower_frame.pack(anchor='n', pady=(44, 0))














a = Second()
a.mainloop()