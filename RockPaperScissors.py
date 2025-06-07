import random
import sys

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

Action = [rock, paper, scissors]

player_choice = input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n")

if player_choice not in ["0", "1", "2"]:
    print("You typed an invalid number, you lose!")
    sys.exit()

player_choice = int(player_choice)
print("You chose:")
print(Action[player_choice])

computer_choice = random.randint(0, 2)
print("Computer chose:")
print(Action[computer_choice])

if player_choice == computer_choice:
    print("It's a draw!")
elif (player_choice == 0 and computer_choice == 2) or \
     (player_choice == 1 and computer_choice == 0) or \
     (player_choice == 2 and computer_choice == 1):
    print("You win!")
else:
    print("You lose!")

