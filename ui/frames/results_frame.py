from ui.base.base_frame import BaseFrame
from ui.base_widgets.big_label import BigLabel
from ui.base_widgets.mid_label import MidLabel
from ui.base_widgets.submit_button import SubmitButton


class ResultsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_widgets()

    def load_widgets(self):
        BigLabel(self, text='Congrats. You finished the quiz.')
        MidLabel(self, textvariable=self.topic_var)
        MidLabel(self, text=f'Total questions: {self.total_questions}')
        MidLabel(self, text='Your score:')
        MidLabel(self, textvariable=self.score_var)
        SubmitButton(self, text='Start new quiz', command=self.on_restart)

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def on_restart(self):
        self.controller.restart_quiz()
        self.master.reset_frames()
        self.on_next_frame(0)
