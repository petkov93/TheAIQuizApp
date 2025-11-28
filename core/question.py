from dataclasses import dataclass


@dataclass
class Question:
    question: str
    options: list[str]
    correct_answer: int
    explanation: str
    user_answer: int = -1

    @classmethod
    def from_dict(cls, d: dict) -> "Question":
        return cls(question=d['question'],
                   options=d['options'],
                   correct_answer=d['answer'],
                   explanation=d['explanation'])

    def check_answer(self, selected_index) -> bool:
        """Checks if the selected answer is the same as the correct answer. Returns True or False"""
        self.user_answer = selected_index
        return self.user_answer == self.correct_answer
