import smtplib
import datetime as dt
import random

# Prompt user for email configuration details
smtp_server = input("Enter SMTP server (e.g., smtp.gmail.com): ")
smtp_port = int(input("Enter SMTP port (usually 587): "))
my_email = input("Enter your email address: ")
password = input("Enter your email password (or app password): ")

# Get current date and time
now = dt.datetime.now()
weekday = now.weekday()  # Monday = 0, Sunday = 6

# Check if today is Monday
if weekday == 0:

    # Read quotes from file and select a random one
    with open("quotes.txt") as quote_file:
        quotes = quote_file.readlines()
        quote = random.choice(quotes)

    # Set up email connection and send the motivational quote
    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()  # Secure the connection
        connection.login(user=my_email, password=password)  # Login to email
        connection.sendmail(
            from_addr=my_email,        # Sender
            to_addrs=my_email,         # Receiver (self, in this case)
            msg=f"Subject:Monday Motivation\n\n{quote}"  # Email content
        )
