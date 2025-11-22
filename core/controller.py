from core.main_app_window import MainWindow
from core.quiz_manager import QuizManager


class QuizController:
    def __init__(self, manager: QuizManager, window: MainWindow | None):
        self.quiz_manager = manager
        self.window = window
        self._frame_index = 0

    def next_frame(self) -> None:
        max_index: int = len(self.window.frame_classes) - 1
        self._frame_index = min(max_index, self._frame_index + 1)
        self.update_shared_vars()
        self.window.show_frame(self._frame_index)

    def restart_quiz(self):
        self._frame_index = 0
        self.window.restart()
        self.quiz_manager.restart()

    def get_current_question(self):
        return self.quiz_manager.current_question

    def get_total_questions(self):
        return self.quiz_manager.total_questions

    def change_question(self, index: int):
        self.quiz_manager.go_to_question(index)

    def submit_answer(self, selected_index: int):
        return self.quiz_manager.submit_answer(selected_index)

    def get_final_score(self):
        return self.quiz_manager.get_final_score()

    def update_shared_vars(self):
        manager = self.quiz_manager
        self.window.topic_var.set(self.window.topic_var.get())
        self.window.total_questions_var.set(manager.total_questions)
        self.window.question_number_var.set(manager.current_question_number)
        self.window.score_var.set(manager.score)
