CURRENCY = "YOUR CURRENCY"  # e.g., "£", "USD", "INR"

class FlightData:
    """
    Represents information about a flight, including price, airports, dates, and number of stops.
    """

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price                          # Total price of the flight
        self.origin_airport = origin_airport        # IATA code of departure airport
        self.destination_airport = destination_airport  # IATA code of arrival airport
        self.out_date = out_date                    # Outbound departure date (YYYY-MM-DD)
        self.return_date = return_date              # Return date (YYYY-MM-DD)
        self.stops = stops                          # Number of stops (0 = direct flight)

def find_cheapest_flight(data):
    """
    Parses the flight offers returned by the Amadeus API and finds the cheapest flight.

    Args:
        data (dict): JSON data from Amadeus API containing flight offers.

    Returns:
        FlightData: Object containing the details of the cheapest flight.
    """

    if not data or not data.get("data"):
        print("No flight data available.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # Initialize the cheapest flight with the first flight in the list
    first_flight = data["data"][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)

    # Iterate through all available flights to find the one with the lowest price
    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])

        if price < lowest_price:
            lowest_price = price
            nr_stops = len(flight["itineraries"][0]["segments"]) - 1  
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date, nr_stops)
            print(f"Lowest price to {destination} is {CURRENCY}{lowest_price}")

    return cheapest_flight
