import json

from core.question import Question
from core.question_fetcher import QuestionFetcher


class QuizManager:
    def __init__(self, total_questions: int):
        self.topic = 'No topic selected.'
        self.score = 0
        self.all_questions: list[Question] = []
        # TODO use this list to show the user which Questions he got wrong
        self.wrong_answers = []
        self.total_questions = total_questions
        self.answered = set()

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
