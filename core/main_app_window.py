from tkinter import StringVar, IntVar

from customtkinter import CTk, set_appearance_mode

from ui.base.base_frame import BaseFrame

# set_appearance_mode('light')
set_appearance_mode('dark')


class MainWindow(CTk):
    def __init__(self, frame_classes: list[type[BaseFrame]]):
        super().__init__()
        self.controller = None
        self.frame_classes = frame_classes

        self.title('The AI Quiz')
        self.geometry('600x600')

        self.frames: dict[type[BaseFrame], BaseFrame] = {}

        # Tk variables to pass around the frames
        self.topic_var = StringVar(value='No topic selected..')
        self.score_var = IntVar(value=0)
        self.question_number_var = IntVar(value=1)
        self.total_questions_var = IntVar(value=0)

    def add_controller(self, controller):
        self.controller = controller

    def show_frame(self, index: int):
        """Creates a frame if not already created, and raises it on top of the stack"""
        if index < 0 or index >= len(self.frame_classes):
            return

        frame_cls = self.frame_classes[index]
        if frame_cls not in self.frames:
            self.create_frame(frame_cls)

        self.frames[frame_cls].tkraise()

    def create_frame(self, frame_class: type[BaseFrame]):
        """Creates a frame from the given frame class"""
        frame: BaseFrame = frame_class(
            self,
            controller=self.controller,
            topic_var=self.topic_var,
            score_var=self.score_var,
            question_number_var=self.question_number_var,
            total_questions_var=self.total_questions_var,
        )
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames[frame_class] = frame

    def restart(self) -> None:
        """Removes all created frames in self.frames"""
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        self.show_frame(0)

    def start(self) -> None:
        """Starts the app mainloop"""
        self.show_frame(0)
        self.mainloop()
