import requests
from datetime import datetime, timedelta
import smtplib
import time

# ------------------------- USER CONFIG -------------------------- #
MY_EMAIL = "<EMAIL>"
MY_PASSWORD = "<PASSWORD>"
SMTP_SERVER = "<SMTP>"
MY_LAT = 20.593683
MY_LONG = 78.962883

# ------------------------- FUNCTION: Check if ISS is Overhead -------------------------- #
def is_iss_overhead():
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])

        if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
            return True
    except Exception as e:
        print(f"ISS API error: {e}")
    return False

# ------------------------- FUNCTION: Check if it is Night -------------------------- #
def is_night():
    try:
        parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }

        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()

        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        # Use UTC time to match API
        time_now = datetime.now()

        if time_now.hour >= sunset or time_now.hour <= sunrise:
            return True
    except Exception as e:
        print(f"Sunrise API error: {e}")
    return False

# ------------------------- MAIN LOOP -------------------------- #
last_sent_time = None
cooldown = timedelta(minutes=30)  # Email once every 30 minutes

while True:
    time.sleep(60)
    now = datetime.now()

    if is_iss_overhead() and is_night():
        # Only send it if no email has been sent recently
        if not last_sent_time or (now - last_sent_time > cooldown):
            try:
                with smtplib.SMTP(SMTP_SERVER) as connection:
                    connection.starttls()
                    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=MY_EMAIL,
                        msg="Subject:Look Up!\n\nThe ISS is above you in the sky!"
                    )
                print(f"Email sent at {now}")
                last_sent_time = now  # Update last sent time
            except Exception as e:
                print(f"Email error: {e}")
