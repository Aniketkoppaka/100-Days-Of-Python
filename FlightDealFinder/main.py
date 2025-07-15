import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# --- INITIALIZATION ---

# Create instances to manage data, perform flight searches, and send notifications
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Define constants for your origin airport and currency symbol
ORIGIN_CITY_IATA = "YOUR CITY IATA CODE"  # e.g., "LON"
CURRENCY = "YOUR CURRENCY"                # e.g., "£", "INR", "$"

# --- UPDATE MISSING IATA CODES ---

# Loop through destinations to fill in missing IATA codes from city names
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)  # Delay to avoid exceeding API rate limits

# Print updated sheet data for debugging
print(f"sheet_data:\n {sheet_data}")

# Update the sheet/database with IATA codes
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# --- GET CUSTOMER EMAILS ---

# Fetch all customer email addresses for notification
customer_data = data_manager.get_customer_emails()
customer_email_list = [row["Email"] for row in customer_data]

# --- DEFINE FLIGHT SEARCH RANGE ---

# Set date range: from tomorrow to 6 months ahead
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6 * 30))

# --- FLIGHT SEARCH AND EMAIL NOTIFICATIONS ---

# Iterate over each destination to find the cheapest flight
for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")

    # Check for direct flights
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )

    # Find the cheapest direct flight
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: {CURRENCY}{cheapest_flight.price}")
    time.sleep(2)  # Pause to respect API rate limits

    # If no direct flight is found, look for flights with stopovers
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,  
            is_direct=False  
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: {CURRENCY}{cheapest_flight.price}")

    # Send notifications if cheaper flight is found
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Compose message based on number of stops
        stops = getattr(cheapest_flight, "stops", 0)  # fallback to 0 if not present
        if stops == 0:
            message = (
                f"Low price alert! Only {CURRENCY}{cheapest_flight.price} to fly direct "
                f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
            )
        else:
            message = (
                f"Low price alert! Only {CURRENCY}{cheapest_flight.price} to fly "
                f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                f"with {stops} stop(s), departing on {cheapest_flight.out_date} "
                f"and returning on {cheapest_flight.return_date}."
            )

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        # Send emails to all customers in the list
        notification_manager.send_emails(
            email_list=customer_email_list,
            email_body=message
        )
