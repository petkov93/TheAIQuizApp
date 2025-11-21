from tkinter import IntVar
from tkinter.messagebox import showerror

from customtkinter import CTkFrame, CTkLabel, CTkRadioButton

from core.question import Question
from helpers.utils import wrap_length
from ui.base_widgets.submit_button import SubmitButton


class QuestionFrame(CTkFrame):
    def __init__(self, master, index, question: Question, on_answer):
        super().__init__(master)
        self.index = index
        self.idx = f'{index + 1}'
        self.question = f"{self.idx}. {question.question}"
        self.options = question.options
        self.correct_answer = question.correct_answer
        self.explanation = question.explanation
        self.user_answer = IntVar(value=question.user_answer)
        self.on_answer = on_answer

        CTkLabel(self, text=self.question, font=('Courier New', 15), wraplength=500)
        self.options_frame = CTkFrame(self)
        SubmitButton(self, text='Submit answer', command=self.on_submit)

        self.load_options()

    def load_options(self):
        options = {
            idx: CTkRadioButton(self.options_frame,
                                text=wrap_length(option, wrap_count=40),
                                value=idx,
                                variable=self.user_answer,
                                font=('Courier New', 15)
                                ).grid(row=idx, column=0, sticky='w', padx=20, pady=5)
            for idx, option in enumerate(self.options)}

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def on_submit(self):
        selected = self.user_answer.get()
        if selected == -1:
            showerror(title='No answer selected', message='Please choose an option before submitting.')
            return
        self.on_answer(self.index, selected)