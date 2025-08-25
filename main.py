from frames import MainWindow
from manager import QuizManager

if __name__ == '__main__':
    app = MainWindow(QuizManager(total_questions=10))
    app.mainloop()

# tkinter colors at:
# https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html