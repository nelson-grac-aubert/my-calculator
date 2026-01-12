allowed_characters = '0123456789+-/*(). '
running = True 

def menu():
    history = []

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
        user_input = input("Enter your mathematical expression composed of only numbers and operators: ")

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
    
    return input_turned_into_list

def check_division_by_0(input_turned_into_list) : 
    """ Checks the list for a division by 0 """
    for i in range (len(input_turned_into_list) - 1) : 
        if input_turned_into_list[i] == "/" and input_turned_into_list[i+1] == "0" : 
            print("Division by 0 is not allowed")
            return False
    return True

def detect_priority(list) : 
    for element in list : 
        if element == "/" or "*" : 
            priority_operation_detected = True 
            break
    return priority_operation_detected

def run_calculator():
    while running:
        checked_expression = check_characters(allowed_characters)
        input_turned_into_list = format_string(checked_expression)
        print(input_turned_into_list)
        if check_division_by_0(input_turned_into_list):
            break
        else:
            print("Please enter a new expression.\n")


if __name__ == "__main__" : 

    menu()

    
        


