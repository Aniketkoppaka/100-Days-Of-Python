from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("MARKETSTACK_API_KEY")
API_URL = "https://api.marketstack.com/v2/eod"

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    error = None
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if not symbol:
            error = "Please enter a stock symbol."
        elif not API_KEY:
            error = "API key is not configured on the server."
        else:
            params = {
                'access_key': API_KEY,
                'symbols': symbol.upper(),
                'limit': 1
            }
            try:
                response = requests.get(API_URL, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("data") and len(data["data"]) > 0:
                    stock_data = data["data"][0]
                else:
                    error = f"No data found for symbol '{symbol}'. Please check the symbol and try again."

            except requests.exceptions.RequestException as e:
                print(f"Error fetching from Marketstack API: {e}")
                error = "Failed to fetch data from the external API. Please try again later."

    return render_template('index.html', stock_data=stock_data, error=error)

if __name__ == "__main__":
    app.run(port=5000, debug=True)



