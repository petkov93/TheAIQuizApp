from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkRadioButton, CTk



class BaseFrame(CTkFrame):
    def __init__(self, master, quiz_manager=None, on_next_frame=None, *,
                 topic_var=None, score_var=None, total_questions_var=None, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        self.topic_var = topic_var
        self.score_var = score_var
        self.total_questions_var = total_questions_var
        self.quiz_manager = quiz_manager
        self.on_next_frame = on_next_frame
        self.all_questions = quiz_manager.all_questions

    def frame_on_top(self) -> bool:
        return self == self.master.winfo_children()[-1]


class SubmitButton(CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs,
                         hover_color='dark green',
                         fg_color='forest green',
                         font=('Aerial', 14), width=200,
                         height=50)


class BigLabel(CTkLabel):
    pass


class MidLabel(BigLabel):
    pass


class SmallLabel(BigLabel):
    pass


class RadioButton(CTkRadioButton):
    pass


class BaseWindow(CTk):
    pass
