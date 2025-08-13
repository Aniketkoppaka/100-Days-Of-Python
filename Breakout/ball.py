from turtle import Turtle

class Ball(Turtle):
    """
    Represents the game ball.
    """
    def __init__(self):
        """Initializes the ball object."""
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.05

    def move(self):
        """Moves the ball by one step."""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Reverses the ball's vertical direction."""
        self.y_move *= -1

    def bounce_x(self):
        """Reverses the ball's horizontal direction."""
        self.x_move *= -1

    def reset_position(self):
        """Resets the ball to the center and reverses its direction."""
        self.goto(0, 0)
        self.move_speed = 0.05
        self.bounce_y()

    def increase_speed(self):
        """Increases the speed of the ball."""
        if self.move_speed > 0.01:
            self.move_speed *= 0.9
