from customtkinter import CTkLabel

from ui.base.base_frame import BaseFrame
from ui.base_widgets.submit_button import SubmitButton


class ResultsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CTkLabel(self, text='Congrats. You finished the quiz.', font=('Aerial', 20))
        CTkLabel(self, textvariable=self.topic_var, font=('Aerial', 16, 'bold'))
        CTkLabel(self, text=f'Total questions: {self.total_questions}', font=('Aerial', 20))
        CTkLabel(self, text='Your score:', font=('Aerial', 20))
        CTkLabel(self, textvariable=self.score_var, font=('Aerial', 16, 'bold'))
        SubmitButton(self, text='Start new quiz', command=self.on_restart)

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def on_restart(self):
        self.controller.restart_quiz()
        self.master.reset_frames()
        self.on_next_frame(0)
