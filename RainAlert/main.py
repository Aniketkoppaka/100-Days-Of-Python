import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# ------------------------- SETUP ------------------------- #

# OpenWeatherMap API endpoint for the 5-day weather forecast (3-hour intervals)
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# Fetching sensitive data from environment variables
api_key = os.environ.get("OWM_API_KEY")           # Your OpenWeatherMap API key
account_sid = os.environ.get("TWILIO_SID")        # Twilio Account SID
auth_token = os.environ.get("AUTH_TOKEN")         # Twilio Auth Token

# Coordinates for the location you want the forecast for (here: India)
weather_params = {
    "lat": 20.593683,
    "lon": 78.962883,
    "appid": api_key,
    "cnt": 4,  # Number of 3-hour forecasts to check (4 = next 12 hours)
}

# ------------------------- FETCH WEATHER DATA ------------------------- #

# Make a GET request to OpenWeatherMap API
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()  # Raise an error if the request failed
weather_data = response.json()  # Parse the JSON response

# ------------------------- CHECK FOR RAIN ------------------------- #

will_rain = False  # Flag to track if rain is expected

# Loop through each forecasted 3-hour block
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    # Weather condition codes < 700 typically mean rain, drizzle, or snow
    if int(condition_code) < 700:
        will_rain = True

# ------------------------- SEND SMS IF RAIN EXPECTED ------------------------- #

if will_rain:
    # Set up a proxy client (only if needed, e.g., on restricted networks)
    proxy_client = TwilioHttpClient()
    https_proxy = os.environ.get("https_proxy")
    if https_proxy:
        proxy_client.session.proxies = {'https': https_proxy}

    # Initialize Twilio client with optional proxy
    client = Client(account_sid, auth_token, http_client=proxy_client)

    # Send SMS alert
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=os.environ.get("TWILIO_FROM"),  # Twilio virtual number
        to=os.environ.get("TWILIO_TO")        # Your verified personal number
    )

    # Print the message status (e.g., "queued", "sent", "delivered")
    print(message.status)

