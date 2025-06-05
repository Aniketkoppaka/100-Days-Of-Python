print("Welcome to the tip calculator!")
bill = float(input("What was the total bill? $"))
tip = int(input("How much tip would you like to give? 10, 12, or 15? "))
people = int(input("How many people to split the bill? "))
Bill_With_Tip = bill + (tip / 100 * bill)
Bill_Split = Bill_With_Tip / people
print(f"Each person should pay: ${Bill_Split:.2f}")
