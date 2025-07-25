import requests
from datetime import datetime
import os

# -------------------- USER DETAILS (Dynamic Input) -------------------- #
# Prompt user for personal details required by Nutritionix
GENDER = input("Enter your gender (male/female): ").strip().lower()
WEIGHT_KG = float(input("Enter your weight in kg: "))
HEIGHT_CM = float(input("Enter your height in cm: "))
AGE = int(input("Enter your age: "))

# -------------------- API CREDENTIALS -------------------- #
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# -------------------- USER INPUT -------------------- #
exercise_text = input("Tell me which exercises you did: ")

# -------------------- REQUEST SETUP -------------------- #
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# -------------------- API CALL TO NUTRITIONIX -------------------- #
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(f"Nutritionix API call: \n {result} \n")

# -------------------- DATE AND TIME -------------------- #
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# -------------------- GOOGLE SHEET SETUP -------------------- #
GOOGLE_SHEET_NAME = "workout"
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]

# -------------------- LOG EACH EXERCISE TO GOOGLE SHEET -------------------- #
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            os.environ["ENV_SHEETY_USERNAME"],
            os.environ["ENV_SHEETY_PASSWORD"],
        )
    )
    print(f"Sheety Response: \n {sheet_response.text}")
