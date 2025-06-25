from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

# Set up the game window
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")

# Turn off automatic updates for smoother animation
screen.tracer(0)

# Create game objects
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

# Paddle controls
screen.listen()
screen.onkey(fun=r_paddle.go_up, key="Up")
screen.onkey(fun=r_paddle.go_down, key="Down")
screen.onkey(fun=l_paddle.go_up, key="w")
screen.onkey(fun=l_paddle.go_down, key="s")

# Game loop
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed) # Control the speed of the ball
    screen.update() # Update the screen Manually
    ball.move() # Move the ball

    # Bounce off top and bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Bounce off paddles (collision detection)
    if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or (ball.distance(l_paddle) < 50 and ball.xcor() < -320):
        ball.bounce_x()

    # Right player misses — left scores
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # Left player misses — right scores
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

# Exit on click after game ends
screen.exitonclick()