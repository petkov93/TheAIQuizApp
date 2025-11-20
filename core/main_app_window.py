from tkinter import StringVar, IntVar

from customtkinter import CTk, set_appearance_mode

from core.controller import QuizController
from ui.base.base_frame import BaseFrame

set_appearance_mode('dark')


# set_appearance_mode('light')


class MainWindow(CTk):
    def __init__(self, controller: QuizController, frame_classes: list[type[BaseFrame]]):
        super().__init__()
        self.controller = controller
        self.quiz_manager = controller.quiz_manager
        self.frame_classes = frame_classes

        self.geometry('600x600')
        self.frames = {}

        self.topic_var = StringVar(value=self.quiz_manager.topic)
        self.score_var = IntVar(value=self.quiz_manager.score)
        self.total_questions = self.quiz_manager.total_questions

        self.show_frame_by_index(self.controller.frame_index)
        self.update_vars_loop()

    def update_vars_loop(self):
        self.topic_var.set(self.quiz_manager.topic)
        self.score_var.set(self.quiz_manager.score)
        self.after(100, self.update_vars_loop)

    def show_frame_by_index(self, index=None):
        if index is None:
            self.next_frame()
            return

        frame_cls = self.frame_classes[index]
        if frame_cls not in self.frames:
            self.create_frame(frame_cls)

        self.frames[frame_cls].tkraise()

    def create_frame(self, frame_class):
        frame: BaseFrame = frame_class(self,
                                       controller=self.controller,
                                       quiz_manager=self.quiz_manager,
                                       on_next_frame=self.show_frame_by_index,
                                       topic_var=self.topic_var,
                                       total_questions=self.total_questions,
                                       score_var=self.score_var)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames[frame_class] = frame

    def next_frame(self):
        next_index = (self.controller.next_frame_index(len(self.frame_classes)))
        self.show_frame_by_index(next_index)

    def reset_frames(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()

    def start(self):
        self.mainloop()
