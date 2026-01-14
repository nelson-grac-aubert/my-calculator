allowed_characters = '0123456789+-//*().%^ \n\r'
running = True 
history = []

def menu():
    """ Prints main menu of the calculator, handles history """
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

def validate_string(allowed_characters):
    """ Gets user input and handles first set of error in the string"""
    while True:
        user_input = input("\nEnter your mathematical expression composed of only numbers and operators: ")

        if user_input == "":
            print("Error: expression is empty.")
            continue

        invalid = False
        for ch in user_input:
            if ch not in allowed_characters:
                print("Error: invalid character.")
                invalid = True
                break
        if invalid:
            continue

        last_non_space = None
        for ch in reversed(user_input):
            if ch not in " \n\r":
                last_non_space = ch
                break
        if last_non_space is None:
            print("Error: expression is empty.")
            continue
        if last_non_space in "+-*/%^.(":
            print("Error: expression cannot end with an operator.")
            continue

        return user_input

def previous_non_space_char(index, checked_string):
    """ Returns the previous element of the formatted list 
    Used to determine if a - is an operator or a negative number """
    previous_index = index - 1
    while previous_index >= 0 and checked_string[previous_index] == " ":
        previous_index -= 1
    if previous_index >= 0:
        return checked_string[previous_index]
    return None

def format_string(checked_string):
    """ Transforms the user input string into a formated list of numbers and operators 
    Calculate function will use that list to operate """
    input_turned_into_list = []
    current_number = ""
    i = 0

    if checked_string[-1] in "+-//*().%^" : 
        print("\nError : expression ends in an operator not followed by a number")
        check_characters(allowed_characters)

    while i < len(checked_string):
        character = checked_string[i]

        if character == "-":
            prev_char = previous_non_space_char(i, checked_string)
            if prev_char is None or prev_char in "+-*/%^(":
                current_number = "-"
                i += 1
                continue

        if character in "0123456789.":
            current_number += character
            i += 1
            continue

        if current_number != "":
            input_turned_into_list.append(current_number)
            current_number = ""

        if character == " ":
            i += 1
            continue

        if character == "/" and i+1 < len(checked_string) and checked_string[i+1] == "/":
            input_turned_into_list.append("//")
            i += 2
            continue

        input_turned_into_list.append(character)
        i += 1

    if current_number != "":
        input_turned_into_list.append(current_number)

    print(f"\nLa liste formatée sur laquelle on va faire les opérations : {input_turned_into_list}")
    return input_turned_into_list

############################# OPERATIONS ####################################################
def multiply(left, right):
    return float(left) * float(right)

def divide(left, right):
    right = float(right)
    if right == 0:
        raise ZeroDivisionError("Division by 0 is not allowed")
    return float(left) / (right)

def add(left, right):
    return float(left) + float(right)

def substract(left, right):
    return float(left) - float(right)

def modulo(left,right):
    return float(left) % float(right)

def divide_whole(left, right):
    right = float(right)
    if right == 0:
        raise ZeroDivisionError("Division by 0 is not allowed")
    return float(left) // (right)

def power(left,right):
    left=float(left)
    right=int(float(right))
    result = left ** right
    return result
############################# OPERATIONS ####################################################

def find_matching_open(expression_list, closing_index):
    """ Finds the index of the opening parenthesis that matches the closing one at closing_index"""
    counter = 0

    i = closing_index

    while i >= 0:
        element = expression_list[i]
        if element == ")":
            counter += 1
        elif element == "(":
            counter -= 1
            if counter == 0:
                return i
        i -= 1

    # If we exit the loop without finding "(" : there is a parenthesis syntax error
    return None

def resolve_parenthesis(expression_list) : 
    """ Detects the parenthesis and resolve them in the right order by calling calculate()
    on them, and then replacing them one by one until none is left """

    while ")" in expression_list : 
        for i in range(len(expression_list)) : 
            if expression_list[i] == ")" : 
                closing_parenthesis_index = i 
                break
        
        opening_parenthesis_index = find_matching_open(expression_list, closing_parenthesis_index)

        inside_parenthesis = expression_list[opening_parenthesis_index + 1 : closing_parenthesis_index]

        replacement = calculate(inside_parenthesis)

        expression_list = (expression_list[:opening_parenthesis_index]
        + [str(replacement)]
        + expression_list[closing_parenthesis_index + 1:])

    print(f"Liste avec un niveau de parenthèses en moins : {expression_list}")
    return expression_list

def pass_power(expression_list):
    """ Transforms the highest priority operations (powers and roots) into their result"""
    result = []
    i = 0

    while i < len(expression_list):
        current_element = expression_list[i]

        if current_element == "^":
            result[-1] = power(result[-1], expression_list[i+1])
            i += 2
            continue

        result.append(current_element)
        i += 1

    return result

def pass_mult_div(expression_list):
    """ Transforms the high priority operations (div, mult, modulo) into their result"""
    result = []
    i = 0

    while i < len(expression_list):
        current_element = expression_list[i]
        match current_element:
            case "*":
                result[-1] = multiply(result[-1], expression_list[i+1])
                i += 2
                continue
            case "/":
                result[-1] = divide(result[-1], expression_list[i+1])
                i += 2
                continue
            case "//":
                result[-1] = divide_whole(result[-1], expression_list[i+1])
                i += 2
                continue
            case "%":
                result[-1] = modulo(result[-1], expression_list[i+1])
                i += 2
                continue
            case _:
                result.append(current_element)
                i += 1

    return result

def pass_add_sub(expression_list):
    """ Transforms the low priority operations (add, sub) into their result"""
    result = float(expression_list[0])
    i = 1

    while i < len(expression_list):
        operator = expression_list[i]
        right = expression_list[i+1]

        match operator:
            case "+":
                result = add(result, right)
            case "-":
                result = substract(result, right)

        i += 2

    return result

def calculate(expression_list):
    """ Calls the calculate functions by order of priority """
    expression_list = pass_power(expression_list)
    print(f"la liste après évaluation des puissances : {expression_list}")
    expression_list = pass_mult_div(expression_list)
    print(f"la liste après évaluation des div/mult/modulo : {expression_list}")
    return pass_add_sub(expression_list)
        
def run_calculator():
    """ Transforms the user input into result, and save both in history
    by calling all the previously established functions """
    global history
    while running:
        checked_expression = validate_string(allowed_characters)
        expression_list = format_string(checked_expression)

        try:
            expression_list = resolve_parenthesis(expression_list)
            result = calculate(expression_list)
            print(f"\nResult: {result}\n")

            history.append(f"{checked_expression} = {result}")

            input("Press Enter to continue...")
            return

        except ZeroDivisionError:
            print("Division by 0 is not allowed. Please enter a new expression.\n")
            continue

if __name__ == "__main__" :
    menu()