from customtkinter import CTkRadioButton

from ui.styles.fonts import radio_button_font


class RadioButton(CTkRadioButton):
    FONT = radio_button_font

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         font=self.FONT)
