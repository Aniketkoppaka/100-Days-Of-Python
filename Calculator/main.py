from art import logo

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}
def calculator():
    print(logo)
    continue_calculating = True
    num1 = float(input("What's the first number?: "))
    while continue_calculating:
        operation = input("Pick an operation(+ or - or * or /): ")
        num2 = float(input("What's the next number?: "))
        result = operations[operation](num1, num2)
        print(f"{num1} {operation} {num2} = {result}")
        choice = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation: ").lower()
        if choice == "y":
            num1 = result
        else:
            continue_calculating = False
            print("\n" * 20)
            calculator()

calculator()









