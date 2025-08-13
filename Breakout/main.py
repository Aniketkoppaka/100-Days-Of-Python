import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from brickmanager import BrickManager
from scoreboard import Scoreboard

# --- Screen Setup ---
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Breakout")
screen.tracer(0)

# --- Game Objects Setup ---
paddle = Paddle((0, -250))
ball = Ball()
brick_manager = BrickManager()
scoreboard = Scoreboard()

# --- Keyboard Bindings ---
screen.listen()
screen.onkey(paddle.go_left, "Left")
screen.onkey(paddle.go_right, "Right")
screen.onkey(paddle.go_left, "a")
screen.onkey(paddle.go_right, "d")

# --- Main Game Loop ---
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detecting collision with the top wall
    if ball.ycor() > 280:
        ball.bounce_y()

    # Detecting collision with side walls
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()

    # Detecting collision with paddle
    if ball.distance(paddle) < 50 and ball.ycor() < -230:
        ball.bounce_y()

    # Detecting collision with a brick
    for brick in brick_manager.bricks:
        if ball.distance(brick) < 35:
            brick.goto(1000, 1000)
            brick_manager.bricks.remove(brick)
            ball.bounce_y()
            scoreboard.increase_score()
            if scoreboard.score % 5 == 0:
                 ball.increase_speed()

    # Detecting when paddle misses the ball
    if ball.ycor() < -280:
        scoreboard.decrease_lives()
        if scoreboard.lives == 0:
            scoreboard.game_over()
            game_is_on = False
        else:
            ball.reset_position()
            paddle.goto(0, -250)

    # Detecting when all bricks are broken
    if not brick_manager.bricks:
        scoreboard.win()
        game_is_on = False

screen.exitonclick()
