from tkinter import StringVar

from customtkinter import CTkFrame, CTkOptionMenu

from data.quiz_topics import TOPICS
from ui.base.base_frame import BaseFrame
from ui.base_widgets.big_label import BigLabel
from ui.base_widgets.mid_label import MidLabel
from ui.base_widgets.small_label import SmallLabel
from ui.base_widgets.submit_button import SubmitButton
from ui.base_widgets.topic_button import TopicButton


class WelcomeFrame(BaseFrame):
    QUESTION_COUNT = ['5', '10', '15', '20']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons_frame: CTkFrame | None = None
        self.topic_buttons: list[TopicButton] = []
        self._num_questions_var = StringVar(value='10')

        self.load_widgets()

    @property
    def num_questions(self):
        return int(self._num_questions_var.get())

    def load_widgets(self):
        BigLabel(self, text='The AI Quiz app v1\nMade by Petko Petkov').pack(pady=(20, 5))
        MidLabel(self, text='Select a topic below:').pack(pady=(0, 5))
        self.buttons_frame = CTkFrame(self)
        self.buttons_frame.pack()
        self.topic_buttons = [TopicButton(self.buttons_frame) for _ in range(len(TOPICS))]
        self.show_topics()
        CTkOptionMenu(self, values=self.QUESTION_COUNT, variable=self._num_questions_var).pack(padx=5, pady=5)
        SmallLabel(self, text='Selected topic:').pack(padx=5, pady=5)
        MidLabel(self, textvariable=self.topic_var).pack(padx=5, pady=5)
        SubmitButton(self, text='Generate Quiz', command=self.generate_quiz).pack(pady=10)

    def show_topics(self):
        for idx, (btn, topic) in enumerate(zip(self.topic_buttons, TOPICS)):
            row = idx // 2
            col = idx % 2
            btn.configure(
                text=topic,
                command=lambda b=btn: self._set_topic(b.cget('text')))
            btn.grid(row=row, column=col, padx=5, pady=5)

    def _set_topic(self, topic):
        self.topic_var.set(topic)

    def generate_quiz(self):
        if "No topic selected" in self.topic_var.get():
            return
        # starts loading screen, when api request is ready -> next frame again
        self.controller.next_frame()
        self.controller.quiz_manager.load_questions(
            self.topic_var.get(),
            num_questions=self.num_questions,
            on_complete=self.on_questions_loaded)

    def on_questions_loaded(self):
        self.controller.next_frame()
