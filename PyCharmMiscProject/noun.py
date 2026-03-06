from customtkinter import *
from PIL import Image

class QuizApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x480")
        self.title('Login Page')
        image = CTkImage(Image.open('First/Images/Rain.png'),
                         size=(300, 480))
        CTkLabel(self, text='', image=image).pack(side='left' , padx=0 , pady=0)

        right_frame = CTkFrame(self, width=300, height=480, fg_color='transparent')
        right_frame.pack_propagate(False)
        right_frame.pack(side='right')

        stats = CTkLabel(right_frame, text='Welcome Back!', font=('Arian Bold', 20))
        stats.pack(anchor='w', pady=(20, 0), padx=20)

        row2 = CTkLabel(right_frame, text='Sign in to your account', font=('Arian Bold', 10))
        row2.pack(anchor='w', pady=(20, 10) ,  padx=20)

        #image = CTkImage(Image.open('5264869051899516771.jpg'),
        #                 size=(20 , 20))
        #CTkLabel(right_frame, text='', image=image).pack(anchor= 'nw', padx=20, pady=10)


        small_frame = CTkFrame(right_frame, width=50, height=50, fg_color='white')
        small_frame.pack_propagate(False)
        small_frame.pack(anchor='nw' , padx=20 , pady=20)


        email_lab = CTkLabel(small_frame , text='Email:' , text_color='purple')
        email_lab.pack(anchor='nw' , pady=10 , padx=10)

        email_entry = CTkEntry(right_frame , height=30 , width=50)
        email_entry.pack(anchor='w', pady=10, padx=10)




app = QuizApp()
app.mainloop()