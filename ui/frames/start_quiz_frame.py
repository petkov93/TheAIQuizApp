from ui.base.base_frame import BaseFrame
from ui.base_widgets.big_label import BigLabel
from ui.base_widgets.mid_label import MidLabel
from ui.base_widgets.submit_button import SubmitButton


class StartQuizFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_widgets()

    def load_widgets(self):
        BigLabel(self, text=f'Generated Quiz on:')
        MidLabel(self, textvariable=self.topic_var)
        MidLabel(self, text=f'Total questions: {self.total_questions_var.get()}')
        SubmitButton(self, text='Start Quiz!', command=self.start_quiz)

        for child in self.winfo_children():
            child.pack(anchor='center', pady=20)

    def start_quiz(self):
        self.controller.next_frame()
