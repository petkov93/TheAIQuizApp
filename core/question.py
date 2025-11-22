class Question:
    def __init__(self, question_data: dict):
        self.question: str = question_data['question']
        self.options: list[str] = question_data['options']
        self.correct_answer: int = question_data['answer']
        self.explanation: str = question_data['explanation']
        self.user_answer: int = -1

    def check_answer(self, selected_index) -> bool:
        """Checks if the selected answer is the same as the correct answer. Returns True or False"""
        self.user_answer = selected_index
        return self.user_answer == self.correct_answer
