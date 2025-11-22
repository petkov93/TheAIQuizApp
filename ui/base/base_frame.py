from abc import ABC, abstractmethod

from customtkinter import CTkFrame


class BaseFrame(CTkFrame, ABC):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, fg_color='transparent', *args)
        self.controller = controller
        self.topic_var = kwargs.get('topic_var', '')
        self.score_var = kwargs.get('score_var', 0)
        self.question_number_var = kwargs.get('question_number_var', 0)
        self.total_questions_var = kwargs.get('total_questions_var', 0)

    @abstractmethod
    def load_widgets(self):
        pass
