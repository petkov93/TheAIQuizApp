from customtkinter import CTkFrame

from data.quiz_topics import TOPICS
from ui.base.base_frame import BaseFrame
from ui.base_widgets.big_label import BigLabel
from ui.base_widgets.mid_label import MidLabel
from ui.base_widgets.small_label import SmallLabel
from ui.base_widgets.submit_button import SubmitButton
from ui.base_widgets.topic_button import TopicButton


class WelcomeFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons_frame: CTkFrame | None = None
        self.topic_buttons: list[TopicButton] = []

        self.load_widgets()

    def load_widgets(self):
        BigLabel(self, text='The AI Quiz app v1\nMade by Petko Petkov').pack(pady=(20, 5))
        MidLabel(self, text='Select a topic below:').pack(pady=(0, 5))
        self.buttons_frame = CTkFrame(self)
        self.buttons_frame.pack()
        self.topic_buttons = [TopicButton(self.buttons_frame) for _ in range(len(TOPICS))]
        self.show_topics()
        SmallLabel(self, text='Selected topic:').pack(padx=5, pady=5)
        MidLabel(self, textvariable=self.topic_var).pack(padx=5, pady=5)
        SubmitButton(self, text='Generate Quiz', command=self.generate_quiz).pack(pady=10)

    def show_topics(self):
        for idx, (btn, topic) in enumerate(zip(self.topic_buttons, TOPICS)):
            row = idx // 2
            col = idx % 2
            btn.configure(
                text=topic,
                command=lambda b=btn: self.set_topic(b.cget('text')))
            btn.grid(row=row, column=col, padx=5, pady=5)

    def set_topic(self, topic):
        self.quiz_manager.topic = topic

    def generate_quiz(self):
        if self.topic_var.get() == 'No topic selected.':
            return
        # starts loading screen, when api request is ready -> next frame again
        self.quiz_manager.fetch_questions(self.on_next_frame)
        self.on_next_frame()

    def on_questions_loaded(self):
        self.controller.next_frame()
