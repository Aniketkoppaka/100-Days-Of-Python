from turtle import Turtle

# Constants
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.reset_position() # Start at bottom of screen
        self.setheading(90) # Point upwards

    def move_up(self):
        # Move the player up by fixed distance
        self.forward(MOVE_DISTANCE)

    def reset_position(self):
        # Reset the player to the bottom of the screen
        self.goto(STARTING_POSITION)
        self.setheading(90)

    def is_at_finish_line(self):
        # Return True if player is at the finish line, False otherwise
        if self.ycor() > FINISH_LINE_Y:
            return True
        else:
            return False


