from core.quiz_manager import QuizManager


class QuizController:
    def __init__(self, manager: QuizManager):
        self.quiz_manager = manager
        self.frame_index = 0

    def next_frame_index(self, max_frames: int) -> int:
        self.frame_index = (self.frame_index + 1) % max_frames
        return self.frame_index

    def go_to_frame(self, index):
        self.frame_index = index

    def restart_quiz(self):
        self.quiz_manager.restart()
        self.frame_index = 0
