from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1 # Lower = faster

    def move(self):
        # Move the ball by x and y deltas
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        # Reverse vertical direction
        self.y_move *= -1

    def bounce_x(self):
        # Reverse horizontal direction and increase speed
        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self):
        # Reset ball to center and randomize direction
        self.goto(0,0)
        self.move_speed = 0.1
        self.bounce_x()


