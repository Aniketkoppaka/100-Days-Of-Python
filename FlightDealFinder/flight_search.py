import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
CURRENCY = "YOUR CURRENCY CODE"

# Amadeus API endpoints
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    """
    Handles communication with the Amadeus API for fetching IATA codes and flight offers.
    """

    def __init__(self):
        # Load credentials from environment
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = None
        self._token_expiry = datetime.min

        # Immediately get a fresh token on initialization
        self._refresh_token()

    def _refresh_token(self):
        """
        Requests a new access token using client credentials flow.
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=AMADEUS_ENDPOINT, headers=headers, data=body)
        response.raise_for_status()

        token_data = response.json()
        self._token = token_data['access_token']
        self._token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'])

        print(f"[Token] New token acquired, expires in {token_data['expires_in']} seconds")

    def _get_headers(self):
        """
        Ensures token is fresh and returns authorization headers.
        """
        if datetime.now() >= self._token_expiry:
            print("[Token] Expired, refreshing...")
            self._refresh_token()
        return {'Authorization': f'Bearer {self._token}'}

    def get_destination_code(self, city_name):
        """
        Given a city name, returns the IATA code for the main airport in that city.
        """
        headers = self._get_headers()

        query = {
            'keyword': city_name,
            'max': 2,
            'include': "AIRPORTS",
        }

        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)

        if response.status_code != 200:
            print(f"[Error] Failed to fetch IATA code for {city_name}. Status: {response.status_code}")
            print(response.text)
            return "N/A"

        try:
            return response.json()["data"][0]['iataCode']
        except (IndexError, KeyError):
            print(f"[Error] No valid airport code found for {city_name}")
            return "N/A"

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """
        Fetches flight offers between origin and destination within the specified date range.
        Returns JSON data with flight options or None if request fails.
        """
        headers = self._get_headers()

        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": CURRENCY,
            "max": "10",
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)

        if response.status_code != 200:
            print(f"[Error] check_flights() failed. Status: {response.status_code}")
            print("Response:", response.text)
            return None

        return response.json()
