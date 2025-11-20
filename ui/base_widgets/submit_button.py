from customtkinter import CTkButton

from ui.styles.fonts import submit_button_font


class SubmitButton(CTkButton):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         hover_color='dark green',
                         fg_color='forest green',
                         font=submit_button_font,
                         width=200,
                         height=50)

