import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DataManager:
    """
    Handles fetching and updating destination and user data using Sheety API.
    """

    def __init__(self):
        # Read Sheety credentials and endpoints from environment variables
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self.prices_endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint = os.environ["SHEETY_USERS_ENDPOINT"]

        # Setup for Basic Auth
        self._authorization = HTTPBasicAuth(self._user, self._password)

        # Cached data placeholders
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        """
        Fetch destination data (city, IATA code, price) from Sheety.
        Returns a list of destination records.
        """
        try:
            response = requests.get(url=self.prices_endpoint, auth=self._authorization)
            response.raise_for_status()
            data = response.json()
            self.destination_data = data["prices"]
            return self.destination_data
        except requests.RequestException as e:
            print(f"[Error] Failed to fetch destination data: {e}")
            return []

    def update_destination_codes(self):
        """
        Update the IATA codes in the Google Sheet via Sheety API.
        Requires self.destination_data to be populated first.
        """
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            try:
                response = requests.put(
                    url=f"{self.prices_endpoint}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                response.raise_for_status()
                print(f"[Success] Updated {city['city']} with IATA: {city['iataCode']}")
            except requests.RequestException as e:
                print(f"[Error] Failed to update {city['city']}: {e}")

    def get_customer_emails(self):
        """
        Fetches user emails from Sheety for notification purposes.
        Returns a list of users with their emails.
        """
        try:
            response = requests.get(url=self.users_endpoint, auth=self._authorization)
            response.raise_for_status()
            data = response.json()
            self.customer_data = data["users"]
            return self.customer_data
        except requests.RequestException as e:
            print(f"[Error] Failed to fetch customer emails: {e}")
            return []
