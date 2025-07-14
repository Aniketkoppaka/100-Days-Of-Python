CURRENCY = "YOUR CYRRENCY"

class FlightData:
    """
    Represents information about a flight, including price, airports, and dates.
    """

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price  # Total price of the flight
        self.origin_airport = origin_airport  # IATA code of departure airport
        self.destination_airport = destination_airport  # IATA code of arrival airport
        self.out_date = out_date  # Departure date (YYYY-MM-DD)
        self.return_date = return_date  # Return date (YYYY-MM-DD)


def find_cheapest_flight(data):
    """
    Parses the API response and finds the cheapest flight.
    
    Parameters:
        data (dict): JSON response from the Amadeus API containing flight offers.

    Returns:
        FlightData: Object containing details of the cheapest available flight.
    """

    # If there's no flight data, return a placeholder object with "N/A"
    if not data or not data.get('data'):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    # Start by assuming the first flight is the cheapest
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    # Store this as the current cheapest flight
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    # Loop through all flights to find a cheaper one
    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            # Update the lowest price and extract new flight details
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

            # Create a new FlightData instance with the cheaper option
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is {CURRENCY}{lowest_price}")

    return cheapest_flight
