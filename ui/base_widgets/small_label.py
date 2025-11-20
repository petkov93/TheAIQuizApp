from customtkinter import CTkLabel, CTkFont

from ui.styles.fonts import small_font


class SmallLabel(CTkLabel):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         font=small_font,
                         )
