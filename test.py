allowed_characters = "0123456789+-/*() "

def check_characters(expression):
    for character in expression:
        if character not in allowed_characters:
            return False
    return True

def calculator():
    while True:
        print("Calculator")
        print("Available operations :")
        print("+  addition")
        print("-  subtraction")
        print("*  multiplication")
        print("/  division")
        print("l  left")

        operation = input("Choice your operation :")

        if operation.lower() == "l":
            print("See you soon")
            break

        if operation not in ["+", "-", "*", "/"]:
            print("Invalid operation")
            continue

        try:
            num1 = float(input("Enter the first number : "))
            num2 = float(input("Enter the second number : "))
        except ValueError:
            print("Error : Please enter valid numbers")
            continue

        if operation == "+":
            print("Result :", num1 + num2)
        elif operation == "-":
            print("Result :", num1 - num2)
        elif operation == "*":
            print("Result :", num1 * num2)
        elif operation == "/":
            if num2 == 0:
                print("Error: division by zero")
            else:
                print("Result :", num1 / num2)


if __name__ == "__main__":
    calculator()


def calculator():
    history = []

    while True:
        print("\n--- CALCULATOR ---")
        print("1 - New calculation")
        print("2 - View history")
        print("3 - Clear history")
        print("4 - Exit")

        choice = input("Your choice: ")

        if choice == "1":

            # Calculs

        elif choice == "2":

            if not history:
                print("History is empty.")
            else:
                print("\n--- History ---")
                for h in history:
                    print(h)

        elif choice == "3":
            history.clear()
            print("History cleared.")

        elif choice == "4":
            print("See you soon!")
            break

        else:
            print("Invalid choice")