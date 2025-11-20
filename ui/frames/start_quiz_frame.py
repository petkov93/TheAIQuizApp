from customtkinter import CTkLabel, CTkButton

from ui.base.base_frame import BaseFrame


class StartQuizFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CTkLabel(self, text=f'Generated Quiz on:', font=('Aerial', 28))
        CTkLabel(self, textvariable=self.topic_var, font=('Aerial', 28, 'underline', 'bold'))
        CTkLabel(self, text='Total questions:', font=('Aerial', 28, 'bold'))
        CTkLabel(self, text=str(self.total_questions), font=('Aerial', 20, 'underline', 'bold'))
        CTkButton(self, text='Start Quiz!', font=('Aerial', 20, 'bold'), command=self.start_quiz)
        for child in self.winfo_children():
            child.pack(anchor='center', pady=20)

    def start_quiz(self):
        self.on_next_frame()
