import json

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

    # TODO remove the class from here, put it in __init__, create the obj in main.py
    def fetch_questions(self, on_complete):
        QuestionFetcher(topic=self.topic,
                        num_of_questions=self.total_questions,
                        callback=lambda raw:
                        self._on_api_callback(raw, on_complete)
                        )

    def _on_api_callback(self, raw_data, on_complete):
        """Converts the raw JSON to Question objects, on_complete moves to the next frame"""
        questions = json.loads(raw_data)['questions']
        for question in questions:
            self.all_questions.append(Question(question))
        if callable(on_complete):
            on_complete()

    def add_point(self):
        self.score += 1

    def record_answer(self, question_index: int, selected_index: int) -> bool:
        """
        Returns True if correct, False if wrong.
        Ignores re-submissions of the same question
        """
        q = self.all_questions[question_index]
        if q.is_answered:
            raise ValueError("Already Answered!")

        q.is_answered = True
        if q.correct_answer == selected_index:
            self.add_point()
            return True
        return False
        #
        # is_correct = selected_index == q['answer']
        #
        # if is_correct:
        #     self.add_point()
        # else:
        #     self.wrong_answers.append({
        #         "index": question_index,
        #         "selected": selected_index,
        #         "correct": q['answer'],
        #         "explanation": q['explanation'],
        #         "question": q['question'],
        #         "options": q['options'],
        #     })
        # self.answered.add(question_index)
        # return is_correct

    def restart(self):
        self.topic = 'No topic selected.'
        self.score = 0
        self.all_questions = []
        self.wrong_answers = []
        self.answered = set()
