import requests
from datetime import datetime

# ====================== CONFIGURATION ======================
USERNAME = input("Enter your Pixela username: ")
TOKEN = input("Enter your Pixela token (keep this secret!): ")
HEADERS = {"X-USER-TOKEN": TOKEN}
PIXELA_ENDPOINT = "https://pixe.la/v1/users"

# ====================== FUNCTION DEFINITIONS ======================

def create_user():
    """Creates a new Pixela user."""
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
    print(response.text)

def create_graph():
    """Prompts user to create a new graph for any activity."""
    graph_id = input("Enter a graph ID (unique, no spaces): ")
    name = input("What activity are you tracking? (e.g., Reading, Coding): ")
    unit = input("Enter the unit (e.g., pages, hours, km): ")
    data_type = input("Enter data type (int, float, or string): ")
    color = input("Choose a graph color (shibafu, momiji, sora, ichou, ajisai, kuro): ")

    graph_config = {
        "id": graph_id,
        "name": name,
        "unit": unit,
        "type": data_type,
        "color": color
    }

    graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
    response = requests.post(url=graph_endpoint, json=graph_config, headers=HEADERS)
    print(response.text)

def add_pixel():
    """Adds a new pixel to the specified graph."""
    graph_id = input("Enter the graph ID to add data to: ")
    date = input("Enter the date (YYYYMMDD) or press Enter for today: ")
    if not date:
        date = datetime.now().strftime("%Y%m%d")
    quantity = input("Enter the quantity for today: ")

    pixel_data = {
        "date": date,
        "quantity": str(quantity)
    }

    pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}"
    response = requests.post(url=pixel_endpoint, json=pixel_data, headers=HEADERS)
    print(response.text)

def update_pixel():
    """Updates an existing pixel in the specified graph."""
    graph_id = input("Enter the graph ID: ")
    date = input("Enter the date to update (YYYYMMDD): ")
    new_quantity = input("Enter the new quantity: ")

    update_data = {
        "quantity": str(new_quantity)
    }

    update_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}/{date}"
    response = requests.put(url=update_endpoint, json=update_data, headers=HEADERS)
    print(response.text)

def delete_pixel():
    """Deletes a pixel from the specified graph."""
    graph_id = input("Enter the graph ID: ")
    date = input("Enter the date to delete (YYYYMMDD): ")

    delete_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{graph_id}/{date}"
    response = requests.delete(url=delete_endpoint, headers=HEADERS)
    print(response.text)

# ====================== MAIN MENU ======================

def main():
    while True:
        print("\n=== Pixela Activity Tracker ===")
        print("1. Create a new Pixela user")
        print("2. Create a new graph for any activity")
        print("3. Add a pixel (log activity)")
        print("4. Update a pixel")
        print("5. Delete a pixel")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            create_user()
        elif choice == '2':
            create_graph()
        elif choice == '3':
            add_pixel()
        elif choice == '4':
            update_pixel()
        elif choice == '5':
            delete_pixel()
        elif choice == '6':
            print("Exiting Pixela Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
