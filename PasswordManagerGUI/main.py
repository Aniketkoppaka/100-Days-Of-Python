from tkinter import *
from tkinter import messagebox
import random
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # Character pools
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")
    symbols = list("!#$%&()*+")

    # Randomly choose characters from each pool
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    # Combine and shuffle all characters
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    # Convert list to string
    password = "".join(password_list)

    # Insert password into Entry field and copy to clipboard
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    # Get input values
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check for empty fields
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        # Confirm before saving
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it okay to save?"
        )

        if is_ok:
            # Write to file
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")

            # Clear input fields
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Logo Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")  # Make sure this file exists
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entry Fields
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2, sticky="ew")
website_entry.focus()  # Focus cursor here on launch

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

# Start the GUI loop
window.mainloop()
