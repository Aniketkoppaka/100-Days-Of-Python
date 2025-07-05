from datetime import datetime
import pandas
import random
import smtplib

my_email = "<EMAIL>"
password = "<PASSWORD>"
smtp_server = "<SMTP_SERVER>"

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

if today_tuple in birthdays_dict:

    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[Name]", birthdays_dict[today_tuple]["name"])

        try:
            with smtplib.SMTP(smtp_server) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=birthdays_dict[today_tuple]["email"],
                    msg=f"Subject:Happy Birthday!\n\n{contents}"
                )
        except Exception as e:
            print(f"Failed to send email: {e}")






