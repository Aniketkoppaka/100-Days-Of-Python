# import smtplib
#
# # Get inputs from the user
# smtp_server = input("Enter SMTP server (e.g., smtp.gmail.com): ")
# smtp_port = int(input("Enter SMTP port (usually 587): "))
# my_email = input("Enter your email address: ")
# password = input("Enter your email password (or app password): ")
# receiver_email = input("Enter receiver's email address: ")
#
# # Email content
# subject = input("Enter subject: ")
# body = input("Enter body: ")
# message = f"Subject:{subject}\n\n{body}"
#
# # Send the email
# with smtplib.SMTP(smtp_server, smtp_port) as connection:
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(
#         from_addr=my_email,
#         to_addrs=receiver_email,
#         msg=message
#     )

import smtplib
import datetime as dt
import random

smtp_server = input("Enter SMTP server (e.g., smtp.gmail.com): ")
smtp_port = int(input("Enter SMTP port (usually 587): "))
my_email = input("Enter your email address: ")
password = input("Enter your email password (or app password): ")

now = dt.datetime.now()
weekday = now.weekday()

if weekday == 0:

    with open("quotes.txt") as quote_file:
        quotes = quote_file.readlines()
        quote = random.choice(quotes)

    with smtplib.SMTP(smtp_server, smtp_port) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Monday Motivation\n\n{quote}"
        )
