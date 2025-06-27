from turtle import Turtle
import random

class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh(snake_segments=[])

    # Move food to a new random location that doesn't overlap with the snake
    def refresh(self, snake_segments):
        while True:
            random_x = random.randint(-280, 280)
            random_y = random.randint(-250, 250)
            if all(segment.distance(random_x, random_y) > 20 for segment in snake_segments):
                self.goto(random_x, random_y)
                break


