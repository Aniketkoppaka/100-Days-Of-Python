from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
# Define color constants for styling the UI
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Pomodoro durations in minutes
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Initialize global variables
reps = 0         # Keeps track of how many sessions have passed
timer = None     # Stores the timer so it can be canceled later

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """Stops the timer, resets UI elements, and restarts the session cycle."""
    global reps, timer
    window.after_cancel(timer)  # Cancel the running timer using its ID
    canvas.itemconfig(timer_text, text="00:00")  # Reset the time display
    timer_label.config(text="Timer", fg=GREEN)   # Reset the label
    check_marks_label.config(text="")            # Clear check marks
    reps = 0  # Reset the repetition counter

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """Starts a work or break session based on the current repetition count."""
    global reps
    reps += 1  # Increment session counter each time this is called

    # Convert durations to seconds
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Determine which type of session to start based on the count
    if reps % 8 == 0:
        # Every 8th rep is a long break
        countdown(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        # Every 2nd rep is a short break (even reps excluding 8)
        countdown(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    else:
        # Odd reps are work sessions
        countdown(work_sec)
        timer_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    """Runs the countdown and updates the UI every second."""
    minute = math.floor(count / 60)      # Calculate remaining minutes
    second = count % 60                  # Calculate remaining seconds

    # Ensure seconds always show two digits (e.g. 09, 08, ...)
    if second < 10:
        second = f"0{second}"

    # Update the canvas timer text
    canvas.itemconfig(timer_text, text=f"{minute}:{second}")

    if count > 0:
        # Schedule the function to run again after 1 second
        global timer
        timer = window.after(1000, countdown, count - 1)
    else:
        # When the countdown finishes, start the next session
        start_timer()

        # Update the check marks (one check per work session)
        marks = ""
        work_sessions = math.floor(reps / 2)  # Only count work sessions
        for _ in range(work_sessions):
            marks += "✔"
        check_marks_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
# Create the main window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)  # Add padding and background color

# Create canvas for tomato image and timer text
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")  # Load the image
canvas.create_image(100, 112, image=tomato_img)  # Center the image
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)  # Place the canvas in the grid

# Timer label (top of the window)
timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
timer_label.grid(column=1, row=0)

# Start button
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Check marks label (bottom of the window)
check_marks_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 16))
check_marks_label.grid(column=1, row=3)

# Run the GUI application
window.mainloop()