from tkinter import IntVar
from tkinter.messagebox import showerror, showinfo, showwarning

from customtkinter import CTkFrame, CTkLabel

from ui.base.base_frame import BaseFrame
from ui.base_widgets.radio_button import RadioButton
from ui.base_widgets.small_label import SmallLabel
from ui.base_widgets.submit_button import SubmitButton

options_mapper = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}


class QuestionFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radio_var = IntVar(value=-1)

        self.load_widgets()

    def load_widgets(self):
        manager = self.controller.quiz_manager
        question = manager.current_question
        header = (f"Question {manager.current_question_number} "
                  f"of {manager.total_questions}  •  "
                  f"Score: {manager.score}")
        SmallLabel(self, text=header)
        CTkLabel(self, text=question.question, font=('Courier New', 15), wraplength=500, anchor='w', justify='left')
        options_frame = CTkFrame(self, fg_color='transparent')

        for idx, option in enumerate(question.options):
            text = f'{options_mapper[idx]}) {option}'
            RadioButton(
                options_frame,
                text=text,
                value=idx,
                variable=self.radio_var,
            ).grid(row=idx, column=0, sticky='w', padx=20, pady=5)

        SubmitButton(self, text="Submit Answer", command=self.on_submit)

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()

        # self.controller.update_shared_vars()
        self.radio_var.set(-1)
        self.load_widgets()

    def on_submit(self):
        selected = self.radio_var.get()
        if selected == -1:
            showerror(
                title='No answer selected',
                message='Please choose an option before submitting.')
            return
        try:
            is_correct = self.controller.submit_answer(selected)
        except ValueError as e:
            showwarning(title=str(e), message=f'{str(e)}')
            return

        question = self.controller.get_current_question()

        if is_correct:
            showinfo(title='Correct!', message=f'You selected:\n{options_mapper[selected]}) {question.options[selected]}\n\n'
                                               f'Explanation:\n{question.explanation}')
        else:
            showerror(
                title='Wrong answer!',
                message=(
                    f'You selected:\n{options_mapper[selected]}) {question.options[selected]}\n\n'
                    f'Correct:\n{options_mapper[question.correct_answer]}) {question.options[question.correct_answer]}\n\n'
                    f'Explanation:\n{question.explanation}\n'
                )
            )

        if self.controller.quiz_manager.is_finished:
            self.controller.next_frame()
        else:
            self.controller.quiz_manager.next_question()
            self.refresh()
