# ✈️ Flight Deal Finder

A Python application that searches for the cheapest flights from a fixed origin city to various international destinations and notifies users via SMS and email when a deal below a specified threshold is found.

## 📌 Features

- ✅ Automatically fetches IATA codes for city names using Amadeus API.
- ✅ Searches for both direct and stopover flights within a custom date range.
- ✅ Compares flight prices to user-defined "lowest acceptable price" thresholds.
- ✅ Sends SMS notifications using Twilio and email alerts via SMTP.
- ✅ Integrates with Google Sheets (via Sheety) to store and manage destination and user data.

## 🛠️ Technologies Used

- **Python 3.10+**
- **Requests** for API interaction
- **Twilio** for sending SMS
- **SMTP** for email delivery
- **Amadeus Self-Service API** for flight data
- **Sheety API** for Google Sheets integration
- **dotenv** for secure environment variable management

## 🧠 Project Structure

```bash
.
├── main.py                     # Main script that orchestrates the search and notification process
├── data_manager.py            # Handles Sheety interactions (data retrieval & updates)
├── flight_search.py           # Communicates with the Amadeus API
├── flight_data.py             # Models the flight information and finds the cheapest option
├── notification_manager.py    # Manages Twilio and email notifications
├── .env                       # Stores API keys and credentials (not committed)
├── README.md                  # Project documentation

