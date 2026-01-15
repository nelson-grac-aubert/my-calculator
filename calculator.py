import json_management

allowed_characters = '0123456789+-//*().%^ \n\r'
running = True 
history = json_management.load_history()

def menu():
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
                for i, h in enumerate(history, 1):
                    print(f"{i}. {h['expression']} = {h['result']}")

        elif choice == "3":
            history.clear()
            json_management.save_history(history)
            print("History cleared.")

        elif choice == "4":
            print("See you soon!")
            break

        else:
            print("\nInvalid choice")

def validate_string(allowed_characters):
    """ Gets user input and handles first set of error in the string """
    while True:
        user_input = input("\nEnter your mathematical expression composed of only numbers and operators: ")

        if user_input == "":
            print("\nError: expression is empty.")
            continue

        invalid = False
        for ch in user_input:
            if ch not in allowed_characters:
                print("\nError: invalid character.")
                invalid = True
                break
        if invalid:
            continue

        last_non_space = None
        for ch in user_input[::-1]:
            if ch not in " \n\r":
                last_non_space = ch
                break
        if last_non_space is None:
            print("\nError: expression is empty.")
            continue
        if last_non_space in "+-*/%^.(":
            print("\nError: expression cannot end with an operator.")
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

    while i < len(checked_string):
        character = checked_string[i]

        if character == "-":
            prev_char = previous_non_space_char(i, checked_string)
            if prev_char is None or prev_char in "+-*//%^(":
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

    return input_turned_into_list

def is_valid_number(element):
    """Returns True if element is a valid decimal number."""
    # Handles negative numbers
    if element.startswith('-'):
        element = element[1:]
    # Empty numbers
    if element == "" or element == ".":
        return False
    # Too many decimal dots in one number
    if element.count('.') > 1:
        return False
    # Final check: all remaining chars must be digits
    return element.replace('.', '').isdigit()

def validate_list(formated_list):
    """ Gets formated list and checks for structural errors """

    operators = {"+", "-", "*", "/", "//", "%", "^"}
    
    # Check parentheses balance
    balance = 0
    for element in formated_list:
        if element == "(":
            balance += 1
        elif element == ")":
            balance -= 1
    if balance != 0:
        print("\nError: parentheses are not balanced.")
        return False
    
    if formated_list[0] in operators - {"-"}:
        print(f"\nError: expression cannot start with this operator : {formated_list[0]}")
        return False

    if formated_list[-1] in operators:
        print("\nError: expression cannot end with an operator.")
        return False

    for i in range(len(formated_list) - 1):
        a, b = formated_list[i], formated_list[i+1]

        if a in operators and b in operators:
            print("\nError: two operators in a row.")
            return False

        if a == "(" and b == ")":
            print("\nError: empty parentheses.")
            return False

        if a == "(" and b in operators - {"-"}:
            print("\nError: operator after '('.")
            return False

        if a in operators and b == ")":
            print("\nError: operator before ')'")
            return False
        
        if is_valid_number(a) and is_valid_number(b):
            print("\nError: missing operator between numbers.")
            return False

        if a not in operators and a not in ["(", ")"] and not is_valid_number(a):
            print(f"\nError: invalid number: {a}")
            return False
        if b not in operators and b not in ["(", ")"] and not is_valid_number(b):
            print(f"\nError: invalid number: {b}")
            return False

    return True

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
    expression_list = pass_mult_div(expression_list)
    return pass_add_sub(expression_list)
        
def run_calculator():
    """ Transforms the user input into result, and save both in history
    by calling all the previously established functions """
    global history
    while running:
        checked_expression = validate_string(allowed_characters)
        expression_list = format_string(checked_expression)
        
        if validate_list(expression_list) == False : 
            continue

        try:
            expression_list = resolve_parenthesis(expression_list)
            result = calculate(expression_list)
            print(f"\nResult: {result}\n")

            history.append({"expression": checked_expression, "result": result})
            json_management.save_history(history)

            input("Press Enter to continue...")
            return

        except ZeroDivisionError:
            print("\nError : division by 0 is not allowed.")
            continue

if __name__ == "__main__" :

    menu()

   
