allowed_characters = '0123456789+-/*(). \n\r'
running = True 
history = []

def menu():
    global history

    while True:
        print("\n--- CALCULATOR ---")
        print("1 - New calculation")
        print("2 - View history")
        print("3 - Clear history")
        print("4 - Exit")

        choice = input("Your choice: ")

        if choice == "1":
            run_calculator()

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

def check_characters(allowed_characters):
    """ Asks for user input 
    If user input has non-allowed characters, displays error message and asks again 
    Returns input string if correct """

    while True:
        user_input = input("\nEnter your mathematical expression composed of only numbers and operators: ")

        invalid_found = False
        
        for character in user_input:
            if character not in allowed_characters:
                print("Allowed characters are digits 0-9 and operators + - / * ()")
                invalid_found = True
                break 

        if not invalid_found:
            return user_input

def format_string(checked_string) : 
    """ Turns user input string into a list of numbers and operators """
    input_turned_into_list = []
    current_number = ""

    for character in checked_string : 
        if character in "0123456789." : 
            current_number += character
        else:
            if current_number != "":
                input_turned_into_list.append(current_number)
                current_number = ""
            if character != " ":
                input_turned_into_list.append(character)

    if current_number != "":
       input_turned_into_list.append(current_number)
    
    print(f"\nLa string formatée sur laquelle on va faire les opérations : {input_turned_into_list}")
    return input_turned_into_list

def multiply(left, right):
    return float(left) * float(right)

def divide(left, right):
    right = float(right)
    if right == 0:
        raise ZeroDivisionError("Division by 0 is not allowed")
    return float(left) / right

def add(left, right):
    return float(left) + float(right)

def substract(left, right):
    return float(left) - float(right)

def run_calculator():
    while running:
        checked_expression = check_characters(allowed_characters)
        expression_list = format_string(checked_expression)

        try:
            result = "ici le résultat quand on aura la fonction pour le calculer"
            print(f"\nResult: {result}\n")
            input("Press Enter to continue...")
            return

        except ZeroDivisionError:
            print("Division by 0 is not allowed. Please enter a new expression.\n")
            continue


if __name__ == "__main__" : 

    menu()

    
        


