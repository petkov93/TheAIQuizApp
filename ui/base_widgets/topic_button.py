from customtkinter import CTkButton

from ui.styles.fonts import small_font


class TopicButton(CTkButton):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
                         height=25,
                         width=200,
                         font=small_font,
                         )
