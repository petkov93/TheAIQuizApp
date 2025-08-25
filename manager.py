import json

from fetcher import QuestionFetcher


class QuizManager:
    def __init__(self, total_questions):
        self.topic = 'No topic selected.'
        self.score = 0
        self.all_questions = []
        # TODO use this list to show the user which Questions he got wrong
        self.wrong_answers = []
        self.total_questions = total_questions
        self.answered = set()

    def fetch_questions(self, on_complete):
        QuestionFetcher(topic=self.topic,
                        num_of_questions=self.total_questions,
                        callback=lambda raw:
                        self._on_api_callback(raw, on_complete)
                        )

    def _on_api_callback(self, raw_data, on_complete):
        self.all_questions = json.loads(raw_data)['questions']
        if callable(on_complete):
            on_complete()

    def add_points(self, points: int = 1):
        self.score += points

    def record_answer(self, question_index: int, selected_index: int) -> bool:
        """
        Returns True if correct, False if wrong.
        Ignores re-submissions of the same question
        """
        if question_index in self.answered:
            q = self.all_questions[question_index]
            return selected_index == q['answer']

        q = self.all_questions[question_index]
        is_correct = selected_index == q['answer']

        if is_correct:
            self.add_points(1)
        else:
            self.wrong_answers.append({
                "index": question_index,
                "selected": selected_index,
                "correct": q['answer'],
                "explanation": q['explanation'],
                "question": q['question'],
                "options": q['options'],
            })
        self.answered.add(question_index)
        return is_correct

    def restart(self):
        self.topic = 'No topic selected.'
        self.score = 0
        self.all_questions = []
        self.wrong_answers = []
        self.answered = set()
