from art import logo

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money" : 0.0
}


def print_report():
    """Prints the current resources."""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']:.2f}")

def check_resources(ingredients):
    """Returns True when order can be made, False if ingredients are insufficient."""
    for item in ingredients:
        if ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True

def process_coins():
    """Returns the total calculated from coins inserted."""
    print("Please insert coins.")
    total = int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return round(total, 2)

def check_transaction(money_received, drink_cost):
    """Return True when the payment is accepted, or False if money is insufficient."""
    if money_received < drink_cost:
        print("Sorry that's not enough money. Money refunded.")
        return False
    change = round(money_received - drink_cost, 2)
    if change > 0:
        print(f"Here is ${change} in change.")
    resources["money"] += drink_cost
    return True

def make_coffee(drink_name, ingredients):
    """Deducts the required ingredients from resources and serves the drink."""
    for item in ingredients:
        resources[item] -= ingredients[item]
    print(f"Here is your {drink_name}. Enjoy!")

is_on = True
print(logo)

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino): ").lower()
    if choice == "off":
        is_on = False
    elif choice == "report":
        print_report()
    elif choice in MENU:
        drink = MENU[choice]
        if check_resources(drink["ingredients"]):
            payment = process_coins()
            if check_transaction(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])
    else:
        print("Invalid input.")





