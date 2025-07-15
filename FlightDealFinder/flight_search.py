import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
CURRENCY = "YOUR CURRENCY CODE"  # e.g., "GBP", "USD", "INR"

# Amadeus API endpoints
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    """
    Handles communication with the Amadeus API:
    - Fetching IATA codes for cities
    - Searching for flight offers
    - Managing OAuth access tokens
    """

    def __init__(self):
        # Load API credentials from environment variables
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = None
        self._token_expiry = datetime.min

        # Get an access token upon initialization
        self._refresh_token()

    def _refresh_token(self):
        """
        Refreshes the access token using client credentials.
        Automatically sets the new token and its expiry.
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
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors

        token_data = response.json()
        self._token = token_data['access_token']
        self._token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'])

        print(f"[Token] New token acquired. Expires in {token_data['expires_in']} seconds.")

    def _get_headers(self):
        """
        Returns valid authorization headers.
        Automatically refreshes the token if expired.
        """
        if datetime.now() >= self._token_expiry:
            print("[Token] Expired. Refreshing...")
            self._refresh_token()

        return {'Authorization': f'Bearer {self._token}'}

    def get_destination_code(self, city_name):
        """
        Returns the IATA code for a given city using the Amadeus location API.
        """
        headers = self._get_headers()
        query = {
            'keyword': city_name,
            'max': 2,
            'include': "AIRPORTS",
        }

        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)

        if response.status_code != 200:
            print(f"[Error] Failed to fetch IATA code for '{city_name}'. Status: {response.status_code}")
            print(response.text)
            return "N/A"

        try:
            return response.json()["data"][0]['iataCode']
        except (IndexError, KeyError):
            print(f"[Error] No valid airport code found for '{city_name}'.")
            return "N/A"

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """
        Searches for flights between origin and destination cities
        within the given time range.
        
        Args:
            origin_city_code (str): IATA code for origin
            destination_city_code (str): IATA code for destination
            from_time (datetime): departure window start
            to_time (datetime): return window end
            is_direct (bool): if True, only include direct flights

        Returns:
            dict or None: JSON response from Amadeus or None if failed
        """
        headers = self._get_headers()
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": CURRENCY,
            "max": "10",
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)

        if response.status_code != 200:
            print(f"[Error] check_flights() failed. Status: {response.status_code}")
            print("Response:", response.text)
            return None

        return response.json()
