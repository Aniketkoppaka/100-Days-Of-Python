import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

COLLEGE_URL = os.getenv("COLLEGE_URL")
COLLEGE_TIMETABLE_URL = os.getenv("COLLEGE_TIMETABLE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

def get_timetable():
    print("🚀 Starting browser and logging in...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(COLLEGE_URL)
        time.sleep(6)

        username_field = driver.find_element(By.ID, 'txtUserName')
        password_field = driver.find_element(By.ID, 'txtPassword')
        login_button = driver.find_element(By.ID, 'login_submitStudent')

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        login_button.click()

        print("✅ Login successful! Navigating to timetable...")
        time.sleep(8)

        driver.get(COLLEGE_TIMETABLE_URL)
        time.sleep(8)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        today_str = datetime.now().strftime("%Y-%m-%d")
        today_cell = soup.find("td", {"data-date": today_str})

        if not today_cell:
            return f"❌ Could not find timetable for {today_str}."

        events = today_cell.find_all("a", class_="fc-time-grid-event")
        schedule_message = f"📅 Your Schedule for {today_str}:\n\n"

        if not events:
            schedule_message += "🎉 No classes today!"
        else:
            for event in events:
                time_tag = event.find("div", class_="fc-time")
                title_tag = event.find("div", class_="fc-title")

                class_time = time_tag.get_text(strip=True) if time_tag else "N/A"
                subject = title_tag.get_text(strip=True) if title_tag else "N/A"

                schedule_message += f"⏰ *{class_time}*: {subject}\n"

        return schedule_message

    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error: Could not fetch the timetable. Please check the script and website."
    finally:
        driver.quit()
        print("🚪 Browser closed.")

def send_whatsapp_message(message):
    if "Error" in message:
        print(message)
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=YOUR_WHATSAPP_NUMBER,
            body=message
        )
        print(f"✅ WhatsApp message sent successfully! SID: {msg.sid}")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")

if __name__ == "__main__":
    schedule = get_timetable()
    if schedule and "Error:" not in schedule:
        send_whatsapp_message(schedule)
    else:
        send_whatsapp_message("Could not retrieve your college schedule today. The script might need an update.")
