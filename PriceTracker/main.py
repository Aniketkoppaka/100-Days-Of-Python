from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
BUY_PRICE = 70.0

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.9",
    "Dnt": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# --- Send HTTP Request ---
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# --- Parse Price ---
price_element = soup.find(class_="a-offscreen")
if not price_element:
    print("❌ Price not found. Amazon may have blocked the request or changed the HTML layout.")
    exit()

try:
    price_text = price_element.get_text()
    price_without_currency = price_text.split("$")[1]
    price_as_float = float(price_without_currency)
    print(f"✅ Current price: ${price_as_float}")
except (IndexError, ValueError):
    print("❌ Couldn't parse price correctly.")
    exit()

# --- Parse Title ---
title_element = soup.find(id="productTitle")
if not title_element:
    print("❌ Product title not found.")
    exit()

title = " ".join(title_element.get_text().split())
print(f"📦 Product: {title}")

# --- Check Price and Send Email ---
if price_as_float < BUY_PRICE:
    print("🔔 Price is below threshold! Sending email...")

    # Validate environment variables
    smtp_address = os.getenv("SMTP_ADDRESS")
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if not smtp_address or not email or not password:
        raise EnvironmentError("Missing one or more required environment variables in .env file.")

    message = f"Subject:Amazon Price Alert!\n\n{title} is on sale for {price_text}!\n{url}"

    try:
        with smtplib.SMTP(smtp_address, port=587) as connection:
            connection.starttls()
            connection.login(email, password)
            connection.sendmail(
                from_addr=email,
                to_addrs=email,
                msg=message
            )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
else:
    print(f"💤 Price is still above ${BUY_PRICE}. No email sent.")
