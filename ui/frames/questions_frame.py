from tkinter.messagebox import showinfo, showerror

from customtkinter import CTkFrame, CTkButton

from ui.base.base_frame import BaseFrame
from ui.base_widgets.submit_button import SubmitButton
from ui.question_frame.question_frame import QuestionFrame


class QuestionsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_index = 0
        self.question_frames = {index: QuestionFrame(self, index, question, on_answer=self.handle_answer) for
                                index, question in
                                enumerate(self.quiz_manager.all_questions)}
        for question in self.question_frames.values():
            question.place(relx=0, rely=0, relwidth=1, relheight=.8)
        self.buttons_frame = CTkFrame(self)
        self.buttons_frame.place(relx=0.5, rely=0.85, anchor='s')
        self.show_question()

        self.buttons = {
            idx: CTkButton(
                self.buttons_frame, text=f'{idx + 1}', width=20, height=25,
                font=('Aerial', 14, 'bold'),
                command=lambda i=idx: self.show_question(i))
            for idx in range(len(self.quiz_manager.all_questions))}

        for idx, btn in self.buttons.items():
            btn.grid(row=0, column=idx, padx=1, pady=1, ipadx=1, ipady=1)
        # TODO make the btn disabled if there are unanswered questions
        self.finish_button = SubmitButton(
            self, text='Finish Quiz', command=self.on_finish).place(relx=0.5, rely=0.95, anchor='s')

    # TODO add lazy loading here also / see MainWindow
    def show_question(self, index=0):
        self.current_index = index
        self.question_frames[self.current_index].tkraise()

    def go_to_next_or_finish(self):
        if self.current_index < len(self.quiz_manager.all_questions) - 1:
            self.show_question(self.current_index + 1)
        else:
            self.on_finish()

    # TODO Add a button to finish the quiz, should be inactive if there are unanswered questions.
    def on_finish(self):
        self.on_next_frame()

    def handle_answer(self, q_index: int, selected_index: int):
        """Called by a QuestionFrame when user hits 'Submit answer'."""
        is_correct = self.quiz_manager.record_answer(q_index, selected_index)
        q = self.quiz_manager.all_questions[q_index]

        if is_correct:
            showinfo(title='Correct!', message=f'{q["explanation"]}')
        else:
            showerror(
                title='Wrong answer!',
                message=(
                    f'You selected: {selected_index}\n'
                    f'Correct: {q["answer"]}\n'
                    f'{q["explanation"]}'
                )
            )
        self.go_to_next_or_finish()
