import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

# Set up the main game screen
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0) # Turn off automatic screen updates

# Initialize game objects
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Set up keyboard controls
screen.listen()
screen.onkey(fun=player.move_up, key="Up")

# Main game loop
game_is_on = True
while game_is_on:
    time.sleep(0.1) # Control game speed
    screen.update() # Refresh screen

    car_manager.create_car() # Create a new car object
    car_manager.move_cars() # Move all cars

    # Check for collision with any car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    # Check if player has reached the top
    if player.is_at_finish_line():
        player.reset_position()
        car_manager.level_up() # Increase car speed
        scoreboard.increase_level() # Increase level

screen.exitonclick()