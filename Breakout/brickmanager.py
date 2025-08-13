from turtle import Turtle

COLORS = ["red", "orange", "yellow", "green", "blue"]

class BrickManager:
    """
    Manages the creation and state of all bricks.
    """
    def __init__(self):
        """Initializes the brick manager and creates the wall of bricks."""
        self.bricks = []
        self.create_bricks()

    def create_bricks(self):
        """Creates the grid of bricks at the top of the screen."""
        for i, color in enumerate(COLORS):
            y_position = 200 - (i * 30)
            for j in range(-350, 351, 75):
                brick = Turtle("square")
                brick.shapesize(stretch_wid=1, stretch_len=3.5)
                brick.color(color)
                brick.penup()
                brick.goto(j, y_position)
                self.bricks.append(brick)
