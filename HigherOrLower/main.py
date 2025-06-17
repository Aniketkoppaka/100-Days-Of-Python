import random
from game_data import data
from art import logo, vs

def format_data(account):
    """Takes the account data and returns the printable format."""
    account_name = account["name"]
    account_description = account["description"]
    account_country = account["country"]
    return f"{account_name}, a {account_description}, from {account_country}"

def is_guess_correct(guess, a_followers, b_followers):
    """Take two account objects and return which has a higher follower count."""
    if a_followers > b_followers:
        return guess == "A"
    else:
        return guess == "B"

print(logo)
score = 0
game_should_continue = True

account_b = random.choice(data)

while game_should_continue:

    account_a = account_b
    account_b = random.choice(data)
    while account_a == account_b:
        account_b = random.choice(data)

    print(f"Compare A: {format_data(account_a)}.")
    print(vs)
    print(f"Against B: {format_data(account_b)}.")

    guess = input("Who has more followers? Type 'A' or 'B': ").upper()
    while guess not in ['A', 'B']:
        guess = input("Invalid input. Please type 'A' or 'B': ").upper()

    print("\n" * 20)
    print(logo)

    account_a_follower_count = account_a["follower_count"]
    account_b_follower_count = account_b["follower_count"]

    is_correct = is_guess_correct(guess, account_a_follower_count, account_b_follower_count)

    if is_correct:
        score += 1
        print(f"You're right! Current score: {score}.")
    else:
        print(f"Sorry, that's wrong. Final score: {score}.")
        game_should_continue = False

