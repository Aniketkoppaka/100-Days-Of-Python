import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")

class DataManager:
    """
    Handles interactions with the Sheety API to fetch and update flight destination data.
    """

    def __init__(self):
        # Read Sheety credentials from environment variables
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]

        # Basic Auth setup for Sheety
        self._authorization = HTTPBasicAuth(self._user, self._password)

        # Placeholder for fetched destination data
        self.destination_data = {}

    def get_destination_data(self):
        """
        Fetches destination data (including city names and IATA codes) from Sheety.
        Returns a list of destination records.
        """
        try:
            response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            data = response.json()
            self.destination_data = data["prices"]
            return self.destination_data
        except requests.RequestException as e:
            print(f"[Error] Failed to fetch destination data: {e}")
            return []

    def update_destination_codes(self):
        """
        Updates the IATA code for each destination in the Sheety sheet.
        Expects `self.destination_data` to be populated with city info.
        """
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            try:
                response = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                response.raise_for_status()
                print(f"[Success] Updated {city['city']} with IATA: {city['iataCode']}")
            except requests.RequestException as e:
                print(f"[Error] Failed to update {city['city']}: {e}")
