from tkinter import IntVar
from tkinter.messagebox import showerror, showinfo, showwarning

from customtkinter import CTkFrame, CTkLabel

from ui.base.base_frame import BaseFrame
from ui.base_widgets.radio_button import RadioButton
from ui.base_widgets.small_label import SmallLabel
from ui.base_widgets.submit_button import SubmitButton

# usually there should be 4 possible answers(a, b, c, d), but the GROQ API sometimes surprises with more or less answers... :D
options_mapper = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}


class QuestionFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radio_var = IntVar(value=-1)
        self.header_label: CTkLabel | None = None
        self.question_label: CTkLabel | None = None
        self.options = []

        self.load_widgets()

    def get_question_data(self):
        manager = self.controller.quiz_manager
        question = manager.current_question
        header = (f"Question {manager.current_question_number} "
                  f"of {manager.total_questions}  •  "
                  f"Score: {manager.score}")
        return question, header

    def load_widgets(self):
        question, header = self.get_question_data()
        self.header_label = SmallLabel(self, text=header)
        self.question_label = CTkLabel(self,
                                       text=question.question,
                                       font=('Courier New', 15),
                                       wraplength=500,
                                       anchor='w',
                                       justify='left')
        options_frame = CTkFrame(self, fg_color='transparent')

        for idx, option in enumerate(question.options):
            text = f'{options_mapper[idx]}) {option}'
            rb = RadioButton(
                options_frame,
                text=text,
                value=idx,
                variable=self.radio_var,
            )
            rb.grid(row=idx, column=0, sticky='w', padx=20, pady=5)
            self.options.append(rb)

        SubmitButton(self, text="Submit Answer", command=self.on_submit)

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def refresh(self):
        question, header = self.get_question_data()
        user_answer = self.controller.get_user_answer()

        # hide all widgets
        for widget in self.winfo_children():
            widget.pack_forget()

        # update widgets with new question data
        self.radio_var.set(user_answer)
        self.header_label.configure(text=header)
        self.question_label.configure(text=question.question)

        for rb, option in zip(self.options, question.options):
            rb.configure(text=option)

        # show widgets again
        for widget in self.winfo_children():
            widget.pack(pady=20, anchor='center')

    def on_submit(self):
        selected = self.radio_var.get()
        # if the question is not answered
        if selected == -1:
            showerror(
                title='No answer selected',
                message='Please choose an option before submitting.')
            return
        # if the question is already answered -> ValueError -> warning
        try:
            is_correct = self.controller.submit_answer(selected)
        except ValueError as e:
            showwarning(title=str(e), message=f'{str(e)}')
            return

        question = self.controller.get_current_question()

        if is_correct:
            showinfo(title='Correct!',
                     message=f'You selected:\n{options_mapper[selected]}) {question.options[selected]}\n\n'
                             f'Explanation:\n{question.explanation}')
        else:
            showerror(
                title='Wrong answer!',
                message=(
                    f'You selected:\n{options_mapper[selected]}) {question.options[selected]}\n\n'
                    f'Correct:\n{options_mapper[question.correct_answer]}) {question.options[question.correct_answer]}\n\n'
                    f'Explanation:\n{question.explanation}\n'))

        if self.controller.quiz_manager.is_finished:
            self.controller.next_frame()
        else:
            self.controller.quiz_manager.next_question()
            self.refresh()
