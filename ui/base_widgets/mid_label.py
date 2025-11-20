from customtkinter import CTkLabel

from ui.styles.fonts import middle_font


class MidLabel(CTkLabel):
    FONT = middle_font

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         font=self.FONT)
