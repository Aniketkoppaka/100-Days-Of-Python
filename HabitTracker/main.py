import requests
from datetime import datetime

# ====================== CONFIGURATION ======================
USERNAME = "YOUR_USERNAME"
TOKEN = "YOUR_SECRET_TOKEN"
GRAPH_ID = "your-graph-id"  # e.g., "cycling1"

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
HEADERS = {"X-USER-TOKEN": TOKEN}

# ====================== FUNCTION DEFINITIONS ======================

def create_user():
    """Create a new Pixela user."""
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
    print(response.text)

def create_graph(graph_id, name="My Graph", unit="Km", data_type="float", color="ajisai"):
    """Create a new graph under the user's account."""
    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
    graph_config = {
        "id": graph_id,
        "name": name,
        "unit": unit,
        "type": data_type,
        "color": color,
    }
    response = requests.post(url=graph_endpoint, json=graph_config, headers=HEADERS)
    print(response.text)

def add_pixel(graph_id, date, quantity):
    """Add a new pixel entry to the graph."""
    pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}"
    pixel_data = {
        "date": date,
        "quantity": str(quantity),
    }
    response = requests.post(url=pixel_endpoint, json=pixel_data, headers=HEADERS)
    print(response.text)

def update_pixel(graph_id, date, quantity):
    """Update an existing pixel entry."""
    update_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}/{date}"
    new_data = {
        "quantity": str(quantity)
    }
    response = requests.put(url=update_endpoint, json=new_data, headers=HEADERS)
    print(response.text)

def delete_pixel(graph_id, date):
    """Delete a pixel entry."""
    delete_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}/{date}"
    response = requests.delete(url=delete_endpoint, headers=HEADERS)
    print(response.text)

# ====================== USAGE EXAMPLES ======================

# Format today's date
today = datetime.now().strftime("%Y%m%d")

# Uncomment and run the following functions as needed:

# Step 1: Create a new user (run only once)
# create_user()

# Step 2: Create a graph (run once per graph)
# create_graph(GRAPH_ID, name="Cycling Tracker", unit="Km", data_type="float", color="ajisai")

# Step 3: Add pixel for today
# kms = input("How many kilometers did you cycle today? ")
# add_pixel(GRAPH_ID, today, kms)

# Step 4: Update today's pixel (if needed)
# update_pixel(GRAPH_ID, today, 5.0)

# Step 5: Delete today's pixel (if needed)
# delete_pixel(GRAPH_ID, today)
