import html

class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0       # Track the current question number
        self.score = 0                 # Track the user's score
        self.question_list = q_list    # List of Question objects
        self.current_question = None   # Will hold the current question

    def still_has_questions(self):
        # Return True if there are more questions left
        return self.question_number < len(self.question_list)

    def next_question(self):
        # Get the next question and increment the counter
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        # Decode any HTML entities in the question text
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        # Compare user answer with correct answer (case-insensitive)
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
