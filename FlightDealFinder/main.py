import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# --- INITIALIZATION ---

# Create instances of classes that handle data, flight searching, and notifications
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Define constants for the origin IATA code and desired currency
ORIGIN_CITY_IATA = "YOUR CITY IATA CODE"  # e.g., "LON" for London
CURRENCY = "YOUR CURRENCY"                # e.g., "£" or "INR"

# --- UPDATE MISSING IATA CODES ---

# Loop through all destinations and fetch missing IATA codes using the API
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)  # Pause to respect API rate limits

# Print updated data for verification
print(f"sheet_data:\n {sheet_data}")

# Update the Google Sheet (or database) with newly retrieved IATA codes
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

customer_data = data_manager.get_customer_emails()
customer_email_list = [row["Email"] for row in customer_data]

# --- SET DATE RANGE FOR SEARCH ---

# Set the date range: from tomorrow to 6 months ahead
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6 * 30))

# --- SEARCH AND NOTIFY FOR CHEAP FLIGHTS ---

# Iterate through each destination and check for cheaper flights
for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")

    # Request available flights from origin to destination within the date range
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )

    # Identify the cheapest option from the returned results
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: {CURRENCY}{cheapest_flight.price}")
    time.sleep(2)  # Pause to avoid API rate limits

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: {CURRENCY}{cheapest_flight.price}")

    # If the new flight is cheaper than what’s in the sheet, send an SMS alert
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Customise the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only {CURRENCY} {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only {CURRENCY} {cheapest_flight.price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Check your email. Lower price flight found to {destination['city']}!")

        # Send emails to everyone on the list
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)
