import tkinter as tk
import random

# --- UI CONSTANTS ---
BG_COLOR = "#F0F8FF"
TEXT_COLOR = "#2F4F4F"
FONT_NAME = "Helvetica"
FONT_SIZE = 16

# --- SAMPLE TEXTS ---
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet. "
    "Learning to type quickly and accurately is a valuable skill in today's digital world. Practice makes perfect.",
    "The sun always shines brightest after the rain. Keep your head up and look for the silver lining in every "
    "cloud. Life is full of challenges, but our attitude determines our altitude. Stay positive and keep moving forward.",
    "Technology has revolutionized the way we live, work, and communicate. From the invention of the printing press "
    "to the rise of the internet, innovation continues to shape our society and push the boundaries of what is possible.",
    "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of "
    "outrageous fortune, or to take arms against a sea of troubles and by opposing end them. A classic dilemma.",
    "The world of finance is complex and ever-changing. Understanding concepts like inflation, interest rates, and "
    "investment strategies can empower individuals to make informed decisions about their financial future and build wealth over time."
]

class TypingSpeedTest:
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.config(padx=40, pady=40, bg=BG_COLOR)

        # --- State Variables ---
        self.sample_text = ""
        self.timer = None
        self.time_left = 60
        self.test_in_progress = False

        # --- UI Setup ---
        self.title_label = tk.Label(
            text="Typing Speed Test",
            font=(FONT_NAME, 32, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # --- Sample Text Display ---
        self.text_display = tk.Text(
            self.root,
            height=5,
            width=60,
            wrap=tk.WORD,
            font=(FONT_NAME, FONT_SIZE),
            padx=10,
            pady=10,
            bd=2,
            relief=tk.GROOVE
        )
        self.text_display.grid(row=1, column=0, columnspan=3, pady=10)
        self.text_display.config(state=tk.DISABLED)  # Make it read-only initially

        # --- User Input Area ---
        self.input_text = tk.Text(
            self.root,
            height=5,
            width=60,
            wrap=tk.WORD,
            font=(FONT_NAME, FONT_SIZE),
            padx=10,
            pady=10,
            bd=2,
            relief=tk.GROOVE
        )
        self.input_text.grid(row=2, column=0, columnspan=3, pady=10)
        self.input_text.bind("<KeyRelease>", self.check_typing)

        # --- Results Display ---
        self.time_label = tk.Label(text=f"Time Left: {self.time_left}", font=(FONT_NAME, 14), bg=BG_COLOR)
        self.time_label.grid(row=3, column=0, sticky="w")

        self.wpm_label = tk.Label(text="WPM: 0", font=(FONT_NAME, 14), bg=BG_COLOR)
        self.wpm_label.grid(row=3, column=1)

        self.accuracy_label = tk.Label(text="Accuracy: 100%", font=(FONT_NAME, 14), bg=BG_COLOR)
        self.accuracy_label.grid(row=3, column=2, sticky="e")

        # --- Restart Button ---
        self.restart_button = tk.Button(
            text="Restart Test",
            font=(FONT_NAME, 14, "bold"),
            command=self.reset_test
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=20)

        self.reset_test()

    def reset_test(self):
        """Resets the test to its initial state."""
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

        self.time_left = 60
        self.test_in_progress = False

        self.time_label.config(text=f"Time Left: {self.time_left}")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100%")
        self.input_text.delete("1.0", tk.END)
        self.input_text.config(state=tk.NORMAL)

        self.sample_text = random.choice(SAMPLE_TEXTS)
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, self.sample_text)
        self.text_display.config(state=tk.DISABLED)

    def check_typing(self, event):
        """Handles key release events to check input and manage the test."""
        if not self.test_in_progress and self.input_text.get("1.0", "end-1c"):
            self.test_in_progress = True
            self.countdown()

        user_input = self.input_text.get("1.0", "end-1c")
        input_len = len(user_input)

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)

        correct_chars = 0
        for i, char in enumerate(self.sample_text):
            tag = ""
            if i < input_len:
                if user_input[i] == char:
                    tag = "correct"
                    correct_chars += 1
                else:
                    tag = "incorrect"
            self.text_display.insert(tk.END, char, tag)

        self.text_display.tag_config("correct", foreground="green")
        self.text_display.tag_config("incorrect", foreground="red")
        self.text_display.config(state=tk.DISABLED)

        if input_len > 0:
            accuracy = (correct_chars / input_len) * 100
            self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")

    def countdown(self):
        """Manages the 60-second countdown timer."""
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time Left: {self.time_left}")

            user_input = self.input_text.get("1.0", "end-1c")
            wpm = (len(user_input) / 5) / ((60 - self.time_left) / 60)
            self.wpm_label.config(text=f"WPM: {int(wpm)}")

            self.timer = self.root.after(1000, self.countdown)
        else:
            self.end_test()

    def end_test(self):
        """Ends the test and displays final results."""
        self.test_in_progress = False
        self.input_text.config(state=tk.DISABLED)

        user_input = self.input_text.get("1.0", "end-1c")
        wpm = (len(user_input) / 5)
        self.wpm_label.config(text=f"Final WPM: {int(wpm)}")

if __name__ == "__main__":
    window = tk.Tk()
    app = TypingSpeedTest(window)
    window.mainloop()
