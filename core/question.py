class Question:
    def __init__(self, question_data: dict):
        self.question = question_data['question']
        self.options = question_data['options']
        self.correct_answer = question_data['answer']
        self.user_answer = -1
        self.explanation = question_data['explanation']
        self.is_answered = False

