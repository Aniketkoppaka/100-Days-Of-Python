from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 20, "normal")

class Scoreboard(Turtle):
    """
    Manages the game's score, lives, and on-screen text.
    """
    def __init__(self):
        """Initializes the scoreboard."""
        super().__init__()
        self.score = 0
        self.lives = 3
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clears and rewrites the score and lives."""
        self.clear()
        self.write(f"Score: {self.score}   Lives: {self.lives}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        """Increases the score by one and updates the display."""
        self.score += 1
        self.update_scoreboard()

    def decrease_lives(self):
        """Decreases lives by one and updates the display."""
        self.lives -= 1
        self.update_scoreboard()

    def game_over(self):
        """Displays the 'Game Over' message."""
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=("Courier", 40, "bold"))

    def win(self):
        """Displays the 'You Win!' message."""
        self.goto(0, 0)
        self.write("YOU WIN!", align=ALIGNMENT, font=("Courier", 40, "bold"))
