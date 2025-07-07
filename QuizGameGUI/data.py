import requests

# API parameters to get 10 true/false questions
parameters = {
    "amount": 10,
    "type": "boolean"
}

# Send a GET request to the Open Trivia DB API
response = requests.get("https://opentdb.com/api.php", params=parameters)
response.raise_for_status()  # Raise exception if the request fails

# Parse the JSON response to extract question data
data = response.json()
question_data = data["results"]
