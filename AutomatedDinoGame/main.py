# Make Sure to Change Values Based on Your Screen Settings
import pyautogui
from PIL import ImageGrab
import time

GAME_REGION = (120, 560, 420, 640)

def is_obstacle():
    screen = ImageGrab.grab(bbox=GAME_REGION)
    pixels = screen.load()

    width = GAME_REGION[2] - GAME_REGION[0]
    height = GAME_REGION[3] - GAME_REGION[1]

    for x in range(0, width, 5):
        for y in range(0, height, 5):
            r, g, b = pixels[x, y]
            if (r, g, b) != (255, 255, 255):
                return True
    return False

def play_game():
    print("Starting in 3 seconds... switch to the Dino game tab!")
    time.sleep(3)

    pyautogui.press("space")

    while True:
        if is_obstacle():
            pyautogui.press("space")
            time.sleep(0.05)

if __name__ == "__main__":
    play_game()

