from core.controller import QuizController
from core.main_app_window import MainWindow
from core.quiz_manager import QuizManager
from ui.frames.loading_frame import LoadingFrame
from ui.frames.questions_frame import QuestionsFrame
from ui.frames.results_frame import ResultsFrame
from ui.frames.start_quiz_frame import StartQuizFrame
from ui.frames.welcome_frame import WelcomeFrame

app_frames = [WelcomeFrame, LoadingFrame, StartQuizFrame, QuestionsFrame, ResultsFrame]

manager = QuizManager()
app = MainWindow(app_frames)
controller = QuizController(manager, app)
app.add_controller(controller)

if __name__ == '__main__':
    app.start()

# tkinter colors at:
# https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
