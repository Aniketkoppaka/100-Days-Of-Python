CURRENCY = "YOUR CURRENCY"

class FlightData:
    """
    Represents information about a flight, including price, airports, stops and dates.
    """

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price  # Total price of the flight
        self.origin_airport = origin_airport  # IATA code of departure airport
        self.destination_airport = destination_airport  # IATA code of arrival airport
        self.out_date = out_date  # Departure date (YYYY-MM-DD)
        self.return_date = return_date  # Return date (YYYY-MM-DD)
        self.stops = stops # Number of stops (0 for direct flights. 1 or more for indirect flights)


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
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Start by assuming the first flight is the cheapest
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    # Store this as the current cheapest flight
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

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
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)
            print(f"Lowest price to {destination} is {CURRENCY}{lowest_price}")

    return cheapest_flight
