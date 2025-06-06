print(r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\ ` . "-._ /_______________|_______
|                   | |o ;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
print("🏴‍☠️ Welcome to Treasure Island! 🏝️")
print("Your mission is to find the legendary hidden treasure of the Crimson Pirate.")
choice1 = input("You're at a fork in the jungle trail. Do you go 'left' toward the thick mist or 'right' into the dark woods?\n").lower()
if choice1 == "left":
    choice2 = input("You arrive at a wide, eerie lake. Do you 'swim' across or 'wait' for something?\n").lower()
    if choice2 == "wait":
        choice3 = input("A mysterious boat arrives and takes you across. You reach three ancient doors: one 'red', one 'yellow', and one 'blue'. Which do you choose?\n").lower()
        if choice3 == "red":
            print("🔥 As soon as you open the red door, a fire trap activates! Game Over.")
        elif choice3 == "yellow":
            print("🏆 You open the yellow door and discover the treasure chamber, overflowing with gold! You found the treasure!")
        elif choice3 == "blue":
            print("💀 The blue door leads to a room full of beasts. You don't make it out... Game Over.")
        else:
            print("⚠️ That's not one of the doors! You hesitated too long and the path vanished. Game Over.")
    else:
        print("🦈 You decide to swim, but the lake is home to hungry sea monsters... Game Over.")
else:
    print("☠️ You head right into the woods and fall into a trap laid by pirates. Game Over.")

