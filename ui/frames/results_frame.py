from ui.base.base_frame import BaseFrame
from ui.base_widgets.big_label import BigLabel
from ui.base_widgets.mid_label import MidLabel
from ui.base_widgets.submit_button import SubmitButton


class ResultsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_widgets()

    def load_widgets(self):
        score, total = self.controller.get_final_score()
        BigLabel(self, text='Congrats. You finished the quiz.')
        MidLabel(self, textvariable=self.topic_var)
        MidLabel(self, text=f'Total questions: {total}')
        MidLabel(self, text=f'Your score: {score}')
        SubmitButton(self, text='Start new quiz', command=self.on_restart)

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def on_restart(self):
        self.controller.restart_quiz()
