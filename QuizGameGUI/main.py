from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

# Convert raw question data into Question objects
question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

# Create the QuizBrain instance with all the questions
quiz = QuizBrain(question_bank)

# Launch the GUI with the quiz logic
quiz_ui = QuizInterface(quiz)
