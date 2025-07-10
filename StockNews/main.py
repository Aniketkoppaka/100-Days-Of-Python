import os
import requests
from twilio.rest import Client

# -------------------- Configuration --------------------

# Stock and company identifiers
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# API endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Load API keys and credentials securely from environment variables
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# Twilio phone numbers
VIRTUAL_TWILIO_NUMBER = os.environ.get("TWILIO_PHONE")
VERIFIED_NUMBER = os.environ.get("MY_PHONE")

# -------------------- Get Stock Data --------------------

# Define parameters for Alpha Vantage stock API
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# Make the request and ensure it succeeds
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()

# Parse the JSON response
data = response.json()

# Check if the required data is present
if "Time Series (Daily)" not in data:
    raise Exception("Stock API response is missing 'Time Series (Daily)' data")

# Extract closing prices for the last two days
daily_data = data["Time Series (Daily)"]
data_list = [value for (key, value) in daily_data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

# -------------------- Calculate Price Change --------------------

# Calculate the difference in closing prices
difference = yesterday_closing_price - day_before_yesterday_closing_price

# Determine the direction of change (up or down)
up_down = "🔺" if difference > 0 else "🔻"

# Calculate percentage change relative to the day before yesterday's price
percentage_difference = round((difference / day_before_yesterday_closing_price) * 100)

# -------------------- Get News Articles if Change > 1% --------------------

# Only proceed if the price movement is significant
if abs(percentage_difference) > 1:

    # Define parameters for NewsAPI
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }

    # Request news articles
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()

    # Validate news response
    if "articles" not in news_data:
        raise Exception("News API response is missing 'articles' data")

    # Get the top 3 articles
    articles = news_data["articles"][:3]

    # Format each article for SMS
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}\nBrief: {article['description']}"
        for article in articles
    ]

    # -------------------- Send Messages via Twilio --------------------

    # Initialize Twilio client
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Send each article as a separate message
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER,
        )
