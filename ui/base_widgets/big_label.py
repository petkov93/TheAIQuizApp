from customtkinter import CTkLabel

from ui.styles.fonts import title_font


class BigLabel(CTkLabel):
    FONT = title_font
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         font=self.FONT)
