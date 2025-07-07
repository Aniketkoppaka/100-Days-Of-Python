from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        # Set up the main window
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score label
        self.score_label = Label(text="Score: 0", fg="white", bg=THEME_COLOR, font=("Arial", 16, "bold"))
        self.score_label.grid(row=0, column=1)

        # Canvas to show the question
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, 125,
            width=280,
            text="Question Text",
            fill=THEME_COLOR,
            font=("Arial", 20, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # True button
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, borderwidth=0, command=self.is_correct)
        self.true_button.grid(row=2, column=0)

        # False button
        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, borderwidth=0, command=self.is_wrong)
        self.false_button.grid(row=2, column=1)

        # Load the first question
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        # Reset canvas color and show the next question if available
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def is_correct(self):
        # Handle when user selects "True"
        self.give_feedback(self.quiz.check_answer("True"))

    def is_wrong(self):
        # Handle when user selects "False"
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        # Show color feedback for correct/incorrect answer, then wait 1s
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)
