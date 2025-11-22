from tkinter.messagebox import askokcancel

from customtkinter import CTkFrame

from ui.base.base_frame import BaseFrame
from ui.base_widgets.nav_button import NavButton
from ui.base_widgets.submit_button import SubmitButton
from ui.frames.question_frame import QuestionFrame


class QuestionsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_frame: QuestionFrame | None = None
        self.buttons_frame: CTkFrame | None = None
        self.finish_button: SubmitButton | None = None

        self.load_widgets()

    def load_widgets(self):
        self.question_frame = QuestionFrame(self, self.controller)
        self.buttons_frame = CTkFrame(self)
        self.question_frame.place(relx=0, rely=0, relwidth=1, relheight=.8)
        self.buttons_frame.place(relx=0.5, rely=0.85, anchor='s')
        total_questions = self.controller.get_total_questions()

        for index in range(total_questions):
            NavButton(self.buttons_frame,
                      text=f'{index + 1}',
                      command=lambda i=index: self.show_question(i),
                      ).grid(row=0, column=index, padx=1, pady=1, ipadx=1, ipady=1)

        self.finish_button = SubmitButton(self,
                                          text='Finish Quiz',
                                          command=self._on_finish
                                          )
        self.finish_button.place(relx=0.5, rely=0.95, anchor='s')

    def show_question(self, index: int):
        self.controller.change_question(index)
        self.question_frame.refresh()
        self.refresh()

    def refresh(self):
        pass

    def _on_finish(self):
        """Callback method for the finish button,
        if there are unanswered questions -> ask user for confirmation to end the quiz."""
        unanswered = self.controller.quiz_manager.get_unanswered_questions()
        is_finish = True
        if unanswered:
            is_finish = askokcancel(
                title='Are you sure ?!',
                message=f'You still have {len(unanswered)} questions left.\n'
                        f"Questions [{', '.join(str(q) for q in unanswered)}] still await your answer..")
        if not is_finish:
            return

        self.controller.next_frame()