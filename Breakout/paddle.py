from turtle import Turtle

PADDLE_WIDTH = 5
PADDLE_HEIGHT = 1
MOVE_DISTANCE = 40

class Paddle(Turtle):
    """
    Represents the player's paddle.
    """
    def __init__(self, position):
        """Initializes the paddle object."""
        super().__init__()
        self.shape("square")
        self.color("cyan")
        self.shapesize(stretch_wid=PADDLE_HEIGHT, stretch_len=PADDLE_WIDTH)
        self.penup()
        self.goto(position)

    def go_left(self):
        """Moves the paddle to the left."""
        if self.xcor() > -350:
            new_x = self.xcor() - MOVE_DISTANCE
            self.goto(new_x, self.ycor())

    def go_right(self):
        """Moves the paddle to the right."""
        if self.xcor() < 350:
            new_x = self.xcor() + MOVE_DISTANCE
            self.goto(new_x, self.ycor())
