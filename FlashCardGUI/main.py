from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---------------------------- DATA LOADING ---------------------------- #
# Try loading the list of words to learn, fallback to the original list if not found
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- NEXT CARD ------------------------------- #
def next_card():
    global current_card, flip_timer
    if len(to_learn) == 0:
        # All words have been learned
        canvas.itemconfig(card_title, text="Congrats!", fill="black")
        canvas.itemconfig(card_word, text="All words learned!", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        return

    # Cancel the previous timer and select a new word
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)

    # Update card with French word
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    # Set a timer to flip the card after 3 seconds
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    # Show the English translation of the current word
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# ---------------------------- WORD KNOWN ------------------------------ #
def is_known():
    # Remove known word from the list and save the updated list
    global to_learn
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP -------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Set up the card flip timer
flip_timer = window.after(3000, func=flip_card)

# Create canvas for flash card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Known (right) button
check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, borderwidth=0, command=is_known)
known_button.grid(row=1, column=1)

# Unknown (wrong) button
cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, borderwidth=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Show the first card
next_card()

# Start the main event loop
window.mainloop()
