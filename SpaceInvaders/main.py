import turtle
import math
import time

# -- Game Constants --
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 20
BULLET_SPEED = 25
ALIEN_SPEED = 2
ALIEN_ROWS = 5
ALIENS_PER_ROW = 10
ALIEN_DROP_DISTANCE = 30
BARRIER_BLOCK_SIZE = 20
BARRIER_UNITS = 4

class GameObject(turtle.Turtle):
    """Base class for all game objects."""
    def __init__(self, shape, color, start_x, start_y):
        super().__init__()
        self.shape(shape)
        self.color(color)
        self.penup()
        self.speed(0)
        self.goto(start_x, start_y)

    def move(self, x, y):
        """Moves the object by x and y."""
        self.goto(self.xcor() + x, self.ycor()+ y)

    def is_collided_with(self, other):
        """Checks for collision with another GameObject."""
        distance = math.sqrt(math.pow(self.xcor() - other.xcor(), 2 ) + math.pow(self.ycor() - other.ycor(), 2))
        return distance < 20

class Player(GameObject):
    """The player's spaceship."""
    def __init__(self):
        super().__init__("triangle", "blue", 0, -250)
        self.shapesize(stretch_wid=1, stretch_len=1.5)
        self.setheading(90)

    def move_left(self):
        if self.xcor() > -SCREEN_WIDTH / 2 + 30:
            self.move(-PLAYER_SPEED, 0)

    def move_right(self):
        if self.xcor() < SCREEN_WIDTH / 2 - 30:
            self.move(PLAYER_SPEED, 0)

class Bullet(GameObject):
    """A bullet fired by the player."""
    def __init__(self):
        super().__init__("square", "yellow", 0, -400)
        self.shapesize(stretch_wid=0.2, stretch_len=0.8)
        self.state = "ready"

    def fire(self, x, y):
        if self.state == "ready":
            self.state = "fire"
            self.goto(x, y + 20)
            self.showturtle()

    def move(self):
        if self.state == "fire":
            self.sety(self.ycor() + BULLET_SPEED)
        if self.ycor() > SCREEN_HEIGHT / 2:
            self.reset_bullet()

    def reset_bullet(self):
        self.hideturtle()
        self.state = "ready"
        self.goto(0, -400)

class Alien(GameObject):
    """An alien invader."""
    def __init__(self, x, y):
        super().__init__("circle", "red", x, y)

class Scoreboard(turtle.Turtle):
    """Displays the score and messages."""
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.speed(0)
        self.hideturtle()
        self.goto(0, 260)
        self.score = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score}", align="center", font=("Courier", 24, "normal"))

    def increase_score(self, points):
        self.score += points
        self.update_score()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 40, "bold"))

class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Space Invaders")
        self.screen.tracer(0)

        self.player = Player()
        self.bullet = Bullet()
        self.scoreboard = Scoreboard()
        self.aliens = []
        self.barriers = []
        self.alien_speed = ALIEN_SPEED

        self.create_aliens()
        self.create_barriers()

        self.screen.listen()
        self.screen.onkeypress(self.player.move_left, "Left")
        self.screen.onkeypress(self.player.move_right, "Right")
        self.screen.onkeypress(self.fire_bullet, "space")

        self.running = True

    def create_aliens(self):
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_PER_ROW):
                x = -225 + (col * 50)
                y = 100 + (row * 50)
                self.aliens.append(Alien(x, y))

    def create_barriers(self):
        barrier_positions = [-200, 0, 200]
        for pos_x in barrier_positions:
            for i in range(BARRIER_UNITS):
                for j in range(BARRIER_UNITS):
                    x = pos_x - (BARRIER_UNITS * BARRIER_BLOCK_SIZE / 2) + (j * BARRIER_BLOCK_SIZE)
                    y = -150 + (i * BARRIER_BLOCK_SIZE)
                    barrier_block = GameObject("square", "green", x, y)
                    barrier_block.shapesize(stretch_wid=0.8, stretch_len=0.8)
                    self.barriers.append(barrier_block)

    def fire_bullet(self):
        self.bullet.fire(self.player.xcor(), self.player.ycor())

    def run(self):
        while self.running:
            self.screen.update()
            time.sleep(0.016)

            self.bullet.move()
            self.move_aliens()
            self.check_collisions()

            if not self.running:
                self.scoreboard.game_over()
                self.screen.update()
                time.sleep(3)

        self.screen.bye()

    def move_aliens(self):
        move_down = False
        for alien in self.aliens:
            alien.setx(alien.xcor() + self.alien_speed)
            if alien.xcor() > SCREEN_WIDTH / 2 - 20 or alien.xcor() < -SCREEN_WIDTH / 2 + 20:
                move_down = True

        if move_down:
            self.alien_speed *= -1
            for a in self.aliens:
                a.sety(a.ycor() - ALIEN_DROP_DISTANCE)

    def check_collisions(self):
        # Bullet & Alien
        for alien in self.aliens[:]:
            if self.bullet.is_collided_with(alien):
                self.bullet.reset_bullet()
                alien.goto(0, 1000)
                self.aliens.remove(alien)
                self.scoreboard.increase_score(10)

        # Bullet & Barrier
        for barrier_block in self.barriers[:]:
            if self.bullet.is_collided_with(barrier_block):
                self.bullet.reset_bullet()
                barrier_block.hideturtle()
                self.barriers.remove(barrier_block)

        # Alien & Player
        for alien in self.aliens:
            if alien.is_collided_with(self.player):
                self.player.hideturtle()
                alien.hideturtle()
                self.running = False
                print("Game Over: Alien touched player!")
                break

        # Alien & Barrier
        for alien in self.aliens:
            for barrier_block in self.barriers[:]:
                if alien.is_collided_with(barrier_block):
                    barrier_block.hideturtle()
                    self.barriers.remove(barrier_block)

        # Alien reaches bottom
        for alien in self.aliens:
            if alien.ycor() < self.player.ycor():
                self.running = False
                print("Game Over: Aliens reached your line of defense!")
                break

        # Player wins
        if not self.aliens:
            self.running = False
            print("Congratulations! You saved the Earth!")

if __name__ == "__main__":
    game = Game()
    game.run()


