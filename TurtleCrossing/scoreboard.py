from turtle import Turtle
FONT = ("Courier", 24, "normal")

# Define font for scoreboard text
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1 # Start at level 1
        self.hideturtle()
        self.penup()
        self.goto(-280, 250) # Scoreboard position
        self.update_scoreboard()

    def update_scoreboard(self):
        # Clear the scoreboard and Update the scoreboard with new level
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self):
        # Increase the level by 1 and update the scoreboard
        self.level += 1
        self.update_scoreboard()

    def game_over(self):
        # Write GAME OVER in the center of the screen
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=FONT)



