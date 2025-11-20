from customtkinter import CTkLabel, CTkFrame, CTkButton

from data.quiz_topics import TOPICS
from ui.base.base_frame import BaseFrame
from ui.base_widgets.submit_button import SubmitButton


class WelcomeFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        CTkLabel(self, text='The AI Quiz app v1\nMade by Petko Petkov', font=('Aerial', 28, 'bold')).pack(pady=(20, 5))
        CTkLabel(self, text='Select a topic below:', font=('Aerial', 16)).pack(pady=(0, 5))
        self.buttons_frame = CTkFrame(self)
        self.buttons_frame.pack()
        self.topic_buttons = [CTkButton(self.buttons_frame) for _ in range(len(TOPICS))]
        self.show_topics()
        CTkLabel(self, text='Selected topic:', font=('Aerial', 16)).pack(padx=5, pady=5)
        CTkLabel(self, textvariable=self.topic_var, font=('Aerial', 16, 'bold')).pack(padx=5, pady=5)
        SubmitButton(self, text='Generate Quiz', command=self.generate_quiz).pack(pady=10)

    def show_topics(self):
        for idx, (btn, topic) in enumerate(zip(self.topic_buttons, TOPICS)):
            row = idx // 2
            col = idx % 2
            btn.configure(
                height=25,
                width=200,
                text=topic,
                font=('Aerial', 16, 'bold'),
                command=lambda b=btn: self.set_topic(b.cget('text'))
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

    def set_topic(self, topic):
        self.quiz_manager.topic = topic

    def generate_quiz(self):
        if self.topic_var.get() == 'No topic selected.':
            return
        # starts loading screen, when api request is ready -> next frame again
        self.quiz_manager.fetch_questions(self.on_next_frame)
        self.on_next_frame()
