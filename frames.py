from tkinter import StringVar, IntVar
from tkinter.messagebox import showinfo, showerror

from customtkinter import CTkFrame, CTkLabel, CTk, CTkButton, CTkRadioButton, set_appearance_mode

from const import TOPICS
from modified_widgets import BaseFrame, SubmitButton
from utils import load_gif_frames, wraplength

# set_appearance_mode('dark')
set_appearance_mode('light')


class MainWindow(CTk):
    def __init__(self, quiz_manager):
        super().__init__()
        self.geometry('600x600')
        self.all_questions = []
        self.frame_classes = [WelcomeFrame, LoadingFrame, StartQuizFrame, QuestionsFrame, ResultsFrame]
        self.frames = {}
        self.frame_index = 0
        self.quiz_manager = quiz_manager

        self.topic = StringVar(value=quiz_manager.topic)
        self.score = IntVar(value=quiz_manager.score)
        self.total_questions = IntVar(value=quiz_manager.total_questions)

        self.show_frame_by_index(self.frame_index)
        self.update_vars()

    def show_frame_by_index(self, index=None):
        if index is not None:
            frame_cls = self.frame_classes[index]
            if frame_cls not in self.frames:
                self.create_frame(frame_cls)

            self.frames[frame_cls].tkraise()
            self.frame_index = index
        else:
            self.next_frame()

    def create_frame(self, frame_class):
        frame = frame_class(self, self.quiz_manager, self.show_frame_by_index,
                            topic_var=self.topic,
                            score_var=self.score,
                            total_questions_var=self.total_questions)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames[frame_class] = frame

    def next_frame(self):
        next_index = (self.frame_index + 1) % len(self.frame_classes)
        self.show_frame_by_index(next_index)

    def update_vars(self):
        self.topic.set(self.quiz_manager.topic)
        self.score.set(self.quiz_manager.score)
        # noinspection PyTypeChecker
        self.after(100, self.update_vars)

    def reset_all_frames(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        self.frame_index = 0


class WelcomeFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CTkLabel(self, text='The AI Quiz app v1\nMade by Petko Petkov', font=('Aerial', 28, 'bold')).pack(pady=(20, 5))
        CTkLabel(self, text='Select a topic below:', font=('Aerial', 16)).pack(pady=(0, 5))
        self.buttons_frame = CTkFrame(self)
        self.buttons_frame.pack()
        self.all_topic_buttons = [CTkButton(self.buttons_frame) for _ in range(len(TOPICS))]
        self.show_topics()
        CTkLabel(self, text='Selected topic:', font=('Aerial', 16)).pack(padx=5, pady=5)
        CTkLabel(self, textvariable=self.topic_var, font=('Aerial', 16, 'bold')).pack(padx=5, pady=5)
        SubmitButton(self, text='Generate Quiz', command=self.generate_quiz).pack(pady=10)

    def show_topics(self):
        for idx, (btn, topic) in enumerate(zip(self.all_topic_buttons, TOPICS)):
            row = idx // 2
            col = idx % 2
            btn.configure(
                height=25,
                width=200,
                text=topic,
                font=('Aerial', 16, 'bold'),
                command=lambda b=btn: self.set_topic(b.cget('text'))
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

    def set_topic(self, topic):
        self.quiz_manager.topic = topic

    def generate_quiz(self):
        if self.topic_var.get() == 'No topic selected.':
            return
            # starts loading screen, when api request is ready -> next frame again
        self.quiz_manager.fetch_questions(self.on_next_frame)
        self.on_next_frame()


class LoadingFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = load_gif_frames('gifs/loading.gif')
        CTkLabel(self, text='Generating the quiz...', font=('Aerial', 28, 'bold'))
        self.gif_label = CTkLabel(self, text=' ')

        self.load_widgets()
        self.animate_gif()

    def load_widgets(self):
        for children in self.winfo_children():
            children.pack(anchor='center', fill='x', expand=True)

    def animate_gif(self, delay=30) -> None:
        def update(idx=0):
            self.gif_label.configure(image=self.frames[idx])
            next_idx = (idx + 1) % len(self.frames)
            if self.frame_on_top():
                self.gif_label.after(delay, update, next_idx)

        update()


class StartQuizFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CTkLabel(self, text=f'Generated Quiz on:', font=('Aerial', 28))
        CTkLabel(self, textvariable=self.topic_var, font=('Aerial', 28, 'underline', 'bold'))
        CTkLabel(self, text='Total questions:', font=('Aerial', 28, 'bold'))
        CTkLabel(self, text=str(len(self.all_questions)), font=('Aerial', 20, 'underline', 'bold'))
        CTkButton(self, text='Start Quiz!', font=('Aerial', 20, 'bold'), command=self.start_quiz)
        for child in self.winfo_children():
            child.pack(anchor='center', pady=20)

    def start_quiz(self):
        self.on_next_frame()


class QuestionsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_index = 0
        self.question_frames = {index: QuestionFrame(self, index, question, on_answer=self.handle_answer) for
                                index, question in
                                enumerate(self.all_questions)}
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
            for idx in range(len(self.all_questions))}

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
        if self.current_index < len(self.all_questions) - 1:
            self.show_question(self.current_index + 1)
        else:
            self.on_finish()

    # TODO Add a button to finish the quiz, should be inactive if there are unanswered questions.
    def on_finish(self):
        self.on_next_frame()

    def handle_answer(self, q_index: int, selected_index: int):
        """Called by a QuestionFrame when user hits 'Submit answer'."""
        is_correct = self.quiz_manager.record_answer(q_index, selected_index)
        q = self.all_questions[q_index]

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


class QuestionFrame(CTkFrame):
    def __init__(self, master, index, question: dict, on_answer):
        super().__init__(master)
        self.index = index
        self.idx = f'{index + 1}'
        self.question = f"{self.idx}. {question['question']}"
        self.options = question['options']
        self.correct_answer = question['answer']
        self.explanation = question['explanation']
        self.user_answer = IntVar(value=-1)
        self.on_answer = on_answer

        CTkLabel(self, text=self.question, font=('Courier New', 15), wraplength=500)
        self.options_frame = CTkFrame(self)
        SubmitButton(self, text='Submit answer', command=self.on_submit)

        self.load_options()

    def load_options(self):
        options = {
            idx: CTkRadioButton(self.options_frame,
                                text=wraplength(option, wrap_count=40),
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


class ResultsFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CTkLabel(self, text='Congrats. You finished the quiz.', font=('Aerial', 20))
        CTkLabel(self, textvariable=self.topic_var, font=('Aerial', 16, 'bold'))
        CTkLabel(self, text='Total questions:', font=('Aerial', 20))
        CTkLabel(self, textvariable=self.total_questions_var, font=('Aerial', 16))
        CTkLabel(self, text='Your score:', font=('Aerial', 20))
        CTkLabel(self, textvariable=self.score_var, font=('Aerial', 16, 'bold'))
        SubmitButton(self, text='Start new quiz', command=self.on_restart)

        for child in self.winfo_children():
            child.pack(pady=20, anchor='center')

    def on_restart(self):
        self.quiz_manager.restart()
        self.master.reset_all_frames()
        self.on_next_frame(0)
