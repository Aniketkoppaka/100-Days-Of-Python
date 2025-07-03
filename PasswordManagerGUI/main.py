from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    # Define character pools
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!#$%&()*+')

    # Randomly select characters from each pool
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    # Combine and shuffle characters
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    # Join into a single string
    password = "".join(password_list)

    # Insert into password field and copy to clipboard
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    # Get user input
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Structure to store new data
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Validate input fields
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            # Try to read existing data
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            # File not found: create and write new data
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # File found: update existing data and write back
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            # Clear input fields
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    # Get the website name and convert to lowercase for consistency
    website = website_entry.get().lower()
    try:
        # Try to open and read the data file
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # Data file not found
        messagebox.showerror(title="Error", message="No Data File Found!")
    else:
        # Search for the website in data
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message="No details for such website exists!")

# ---------------------------- UI SETUP ------------------------------- #

# Create main window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Logo image
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")  # Ensure logo.png is in the same directory
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entry fields
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, sticky="ew")
website_entry.focus()  # Automatically focus on this field

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
email_entry.insert(0, "aniket@gmail.com")  # Default email

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="ew")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="ew")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="ew")

# Run the application
window.mainloop()
