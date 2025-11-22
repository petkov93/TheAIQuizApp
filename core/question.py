class Question:
    def __init__(self, question_data: dict):
        self.question = question_data['question']
        self.options = question_data['options']
        self.correct_answer = question_data['answer']
        self.user_answer = -1
        self.explanation = question_data['explanation']
        self.is_answered = False

    def check_answer(self, selected_index) -> bool:
        """Checks if the selected answer is the same as the correct answer. Returns True or False"""
        self.user_answer = selected_index
        return self.user_answer == self.correct_answer
