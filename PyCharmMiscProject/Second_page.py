from customtkinter import *
from Frames import Upper_frame, Middle_frame, Lower_Frame, Additional_info_frame
from PIL import Image

mb = 'Montserrat SemiBold'
m = 'Montserrat'
tr = 'transparent'

class Second(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x1252")
        self.title("ZetaX")
        self.configure(bg="#080451")


        upper_frame = Upper_frame(self)
        upper_frame.pack(anchor='n', pady=(23, 0))

        scroll_frame = CTkScrollableFrame(self, width=1400, height=1252, fg_color="#080451",
                                          corner_radius=59, border_color="#FFFFFF", border_width=1)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        kroshki_frame = CTkFrame(scroll_frame, fg_color=tr)
        kroshki_frame.pack(anchor='nw', padx=25)

        CTkLabel(kroshki_frame, text="Home", font=(mb, 14)).grid(column=0, row=0
                                                                 )
        chevron_image = CTkImage(Image.open('Icons/chevron.png'), size=(24, 24))
        CTkLabel(kroshki_frame, image=chevron_image, text="").grid(column=1, row=0, padx=14)

        CTkLabel(kroshki_frame, text="Bishkek", font=(mb, 14)).grid(column=2, row=0)
        middle_frame = Middle_frame(scroll_frame)
        middle_frame.pack(anchor='n', pady=(10, 0))
        middle_frame.pack_propagate(False)

        add_info = Additional_info_frame(scroll_frame)
        add_info.pack(anchor='n', pady=(83, 0))
        add_info.pack_propagate(False)

        CTkLabel(scroll_frame, text='Extended 14-Day Outlook',
                 font=('Monteserrat', 48)).pack(anchor='n', pady=(57, 0))

        lower_frame = Lower_Frame(scroll_frame)
        lower_frame.pack(anchor='n', pady=(44, 0))


if __name__ == "__main__":
    a = Second()
    a.mainloop()
