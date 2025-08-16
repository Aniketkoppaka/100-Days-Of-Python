import tkinter as tk
from tkinter import font

INACTIVITY_SECONDS = 5
WINDOW_TITLE = "The Most Dangerous Writing App"
WINDOW_GEOMETRY = "900x700"

class DangerousWritingApp:
    """
    A writing application that deletes all text if the user stops typing
    for a specified amount of time.
    """
    def __init__(self, root):
        """
        Initializes the application, sets up the UI, and starts the timer.
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.time_left = INACTIVITY_SECONDS
        self.timer_job = None
        self.setup_ui()
        self.text_area.bind("<KeyPress>", self.reset_timer)
        self.update_timer()

    def setup_ui(self):
        """
        Sets up the visual elements of the application (widgets, colors, fonts).
        """
        BG_COLOR = "#282c34"
        TEXT_COLOR = "#abb2bf"
        TIMER_COLOR = "#e06c75"
        CURSOR_COLOR = "#ffffff"
        SELECT_BG = "#3e4451"

        self.root.configure(bg=BG_COLOR)

        main_font = font.Font(family="Consolas", size=14)
        timer_font = font.Font(family="Courier New", size=18, weight="bold")

        self.timer_label = tk.Label(
            self.root,
            text=f"Time left: {self.time_left}s",
            font=timer_font,
            bg=BG_COLOR,
            fg=TIMER_COLOR
        )
        self.timer_label.pack(pady=20)

        self.text_area = tk.Text(
            self.root,
            wrap=tk.WORD,
            font=main_font,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            insertbackground=CURSOR_COLOR,
            selectbackground=SELECT_BG,
            selectforeground=TEXT_COLOR,
            borderwidth=0,
            highlightthickness=0,
            padx=20,
            pady=20
        )
        self.text_area.pack(expand=True, fill='both')
        self.text_area.focus_set()

    def update_timer(self):
        """
        This method is the core of the timer logic. It runs every second,
        decrements the timer, and checks if the time has run out.
        """
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")

            if self.time_left == 0:
                self.clear_text()
                self.timer_label.config(text="You stopped. Progress lost. Start again.")

        self.timer_job = self.root.after(1000, self.update_timer)

    def reset_timer(self, event=None):
        """
        This method is called every time a key is pressed in the text area.
        It resets the countdown to its initial value.
        """
        self.time_left = INACTIVITY_SECONDS
        self.timer_label.config(text=f"Time left: {self.time_left}s")

    def clear_text(self):
        """
        Deletes all text from the text area.
        """
        self.text_area.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()
