from datetime import datetime
import pandas
import random
import smtplib

# Email credentials and SMTP server info
my_email = "<EMAIL>"
password = "<PASSWORD>"
smtp_server = "<SMTP_SERVER>"

# Get today's date as (month, day)
today = datetime.now()
today_tuple = (today.month, today.day)

# Load birthday data from CSV
data = pandas.read_csv("birthdays.csv")

# Create a dictionary with (month, day) as keys and the entire row as values
birthdays_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

# Check if today's date matches any birthday in the dictionary
if today_tuple in birthdays_dict:

    # Choose a random birthday letter template
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    # Open the selected template and personalize it with the person's name
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[Name]", birthdays_dict[today_tuple]["name"].strip())

        try:
            # Set up connection to SMTP server
            with smtplib.SMTP(smtp_server) as connection:
                connection.starttls()  # Secure the connection
                connection.login(user=my_email, password=password)

                # Send the personalized birthday email
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=birthdays_dict[today_tuple]["email"],
                    msg=f"Subject:Happy Birthday!\n\n{contents}"
                )

        except Exception as e:
            # Print an error message if email sending fails
            print(f"Failed to send email: {e}")
