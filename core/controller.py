from core.quiz_manager import QuizManager


class QuizController:
    def __init__(self, manager: QuizManager):
        self.quiz_manager = manager
        self.frame_index = 0

    def next_frame(self) -> None:
        max_index: int = len(self.window.frame_classes) - 1
        self._frame_index = min(max_index, self._frame_index + 1)
        self.update_shared_vars()
        self.window.show_frame(self._frame_index)

    def restart_quiz(self):
        self.quiz_manager.restart()
        self.frame_index = 0
