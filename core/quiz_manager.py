import json
from collections.abc import Callable

from core.question import Question
from core.question_fetcher import QuestionFetcher


class QuizManager:
    def __init__(self):
        self._questions: list[Question] = []
        self._current_index: int = 0
        self._score: int = 0
        self._answered_indices: set[int] = set()

    @property
    def score(self) -> int:
        return self._score

    @property
    def total_questions(self):
        return len(self._questions)

    @property
    def current_question(self) -> Question:
        if not self._questions:
            raise ValueError("No questions loaded yet!")
        return self._questions[self._current_index]

    @property
    def current_question_number(self) -> int:
        return self._current_index + 1

    @property
    def is_finished(self) -> bool:
        return len(self._questions) == len(self._answered_indices)

    # quiz logic
    def submit_answer(self, selected_index: int) -> bool:
        """Submit answer for current question. Returns True if correct."""
        if self._current_index in self._answered_indices:
            raise ValueError("Already Answered!")

        is_correct = self.current_question.check_answer(selected_index)
        self._answered_indices.add(self._current_index)
        if is_correct:
            self._score += 1

        return is_correct

    def next_question(self) -> None:
        if not self.is_finished:
            while self._current_index in self._answered_indices:
                self._current_index = (self._current_index + 1) % len(self._questions)

    def go_to_question(self, index: int) -> None:
        if 0 <= index < len(self._questions):
            self._current_index = index

    def get_final_score(self) -> tuple[int, int]:
        return self._score, self.total_questions

    def get_unanswered_questions(self):
        return [idx + 1 for idx in range(len(self._questions)) if idx not in self._answered_indices]

    # load questions from AI API
    # TODO remove the class from here, put it in __init__, create the obj in main.py
    def load_questions(self, topic: str, num_questions: int, on_complete: Callable[[], None]) -> None:
        QuestionFetcher(topic=topic,
                        num_of_questions=num_questions,
                        callback=lambda raw:
                        self._handle_api_response(raw, on_complete)
                        )

    def _handle_api_response(self, raw_data: str, on_complete: Callable[[], None]) -> None:
        """Converts the raw JSON to Question objects, on_complete moves to the next frame"""
        data = json.loads(raw_data)

        questions = data['questions']
        for q in questions:
            self._questions.append((Question.from_dict(q)))
        if callable(on_complete):
            on_complete()

    def restart(self):
        self._current_index = 0
        self._score = 0
        self._answered_indices.clear()
        self._questions = []
