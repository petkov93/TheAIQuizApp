from customtkinter import CTkButton

from ui.styles.fonts import nav_font


class NavButton(CTkButton):
    FONT = nav_font
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         width=20,
                         height=25,
                         font=self.FONT
                         )