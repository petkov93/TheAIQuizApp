from collections.abc import Callable

from customtkinter import CTkFrame

from core.controller import QuizController
from core.quiz_manager import QuizManager


class BaseFrame(CTkFrame):
    def __init__(self, master, controller: QuizController, quiz_manager: QuizManager, on_next_frame: Callable, *args,
                 **kwargs):
        super().__init__(master, fg_color='transparent', *args)
        self.controller = controller
        self.quiz_manager = quiz_manager
        self.on_next_frame = on_next_frame
        self.topic_var = kwargs['topic_var']
        self.score_var = kwargs['score_var']
        self.total_questions = kwargs['total_questions']
