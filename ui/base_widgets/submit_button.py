from customtkinter import CTkButton


class SubmitButton(CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         hover_color='dark green',
                         fg_color='forest green',
                         font=('Aerial', 14), width=200,
                         height=50)

