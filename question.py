class QuestionData:
    # TODO implement this class instead of dictionary ;)
    def __init__(self, question_data: dict):
        self.question = question_data['question']
        self.options = question_data['options']
        self.correct_answer = question_data['answer']
        self.explanation = question_data['explanation']

