from tkinter import *
import requests

# Function to fetch and display a quote from the Kanye REST API
def get_quote():
    # Fetch the quote from the API
    response = requests.get("https://api.kanye.rest")
    response.raise_for_status()
    data = response.json()
    quote = data["quote"]

    # Adjust font size based on quote length to keep it readable
    if len(quote) > 120:
        canvas.itemconfig(quote_text, font=("Arial", 14, "bold"))
    elif len(quote) > 80:
        canvas.itemconfig(quote_text, font=("Arial", 16, "bold"))
    else:
        canvas.itemconfig(quote_text, font=("Arial", 20, "bold"))

    # Update the quote text on the canvas
    canvas.itemconfig(quote_text, text=quote)


# ---------------------------- UI SETUP ------------------------------- #

# Create the main application window
window = Tk()
window.title("Kanye Says...")
window.config(padx=50, pady=50)

# Create canvas for background and quote text
canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)  # Centered background image

# Create the text element in the center of the canvas
quote_text = canvas.create_text(
    150, 207,
    text="Kanye Quote Goes HERE",
    width=250,  # Wrap text within this width
    font=("Arial", 30, "bold"),
    fill="white"
)
canvas.grid(row=0, column=0)

# Create the button with Kanye image that fetches a new quote
kanye_img = PhotoImage(file="kanye.png")
kanye_button = Button(
    image=kanye_img,
    highlightthickness=0,
    borderwidth=0,
    command=get_quote
)
kanye_button.grid(row=1, column=0)

# Fetch and display the first quote when the app starts
get_quote()

# Start the main event loop
window.mainloop()
