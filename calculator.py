import json_management
from tkinter import messagebox

allowed_characters = '0123456789+-//*().%^ \n\r'
running = True 
history = json_management.load_history()

def display_error(msg):
    """ Prints error in terminal, or in window if using GUI """
    if USE_GUI:
        messagebox.showerror("Error", msg)
    else:
        print(msg)

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
                display_error("History is empty.")
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
    """ Handles errors that can be detected in the string """
    while True:
        user_input = input("\nEnter your mathematical expression composed of only numbers and operators: ")

        if user_input == "":
            display_error("\nError: expression is empty.")
            continue

        invalid = False
        for character in user_input:
            if character not in allowed_characters:
                display_error("\nError: invalid character.")
                invalid = True
                break
        if invalid:
            continue
        
        last_non_space = None
        for character in user_input[::-1]:
            if character not in " \n\r":
                last_non_space = character
                break
        if last_non_space is None:
            display_error("\nError: expression is empty.")
            continue
        if last_non_space in "+-*/%^.(":
            display_error("\nError: expression cannot end with an operator.")
            continue

        return user_input

def previous_non_space_char(index, checked_string):
    """ Returns the previous element of the formated list 
    Used to determine if a - is an operator or a negative number """
    previous_index = index - 1
    while previous_index >= 0 and checked_string[previous_index] == " ":
        previous_index -= 1
    if previous_index >= 0:
        return checked_string[previous_index]
    return None

def next_non_space_index(index, checked_string):
    """ Return the index of the next non-space character at or after `index`,
    or None if none exists. """
    i = index
    L = len(checked_string)
    while i < L and checked_string[i] == " ":
        i += 1
    return i if i < L else None

def format_string(checked_string):
    """ Transforms the user input string into a formated list of numbers and operators """
    input_turned_into_list = []
    current_number = ""
    i = 0
    L = len(checked_string)

    while i < L:
        character = checked_string[i]

        # Handle - (...) with possible spaces
        if character == "-":
            prev_char = previous_non_space_char(i, checked_string)

            # If next non-space is "(" -> convert to -1 * (
            j = next_non_space_index(i + 1, checked_string)
            if j is not None and checked_string[j] == "(":
                input_turned_into_list.append("-1")
                input_turned_into_list.append("*")
                i = j  # position on '('
                continue

            # If previous token allows - , start building negative number
            if prev_char is None or prev_char in "+-*/%^(":
                # set current_number to "-" and try to consume following spaces+digits/dot
                current_number = "-"
                i += 1
                # skip spaces but keep i at first non-space to continue number parsing
                while i < L and checked_string[i] == " ":
                    i += 1
                # if next is digit or dot, continue loop to collect digits
                if i < L and checked_string[i] in "0123456789.":
                    continue
                # if next is "(" we already handled above; otherwise leave "-" to be validated later
                continue

        # Number characters, digits or dot
        if character in "0123456789.":
            current_number += character
            i += 1
            continue

        # If we have been building a number, finalize it before handling other tokens
        if current_number != "":
            input_turned_into_list.append(current_number)
            current_number = ""

        # Skip spaces
        if character == " ":
            i += 1
            continue

        # Handle '//' operator
        if character == "/" and i + 1 < L and checked_string[i + 1] == "/":
            input_turned_into_list.append("//")
            i += 2
            continue

        # Append single-character operator or parenthesis
        input_turned_into_list.append(character)
        i += 1

    # Finish by appending last number
    if current_number != "":
        input_turned_into_list.append(current_number)
    
    print(input_turned_into_list)
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
    
    # Parentheses balance
    balance = 0
    for element in formated_list:
        if element == "(":
            balance += 1
        elif element == ")":
            balance -= 1
    if balance != 0:
        display_error("\nError: parentheses are not balanced.")
        return False
    
    # Operator at start or end of expression
    if formated_list[0] in operators - {"-"}:
        display_error(f"\nError: expression cannot start with this operator : {formated_list[0]}")
        return False

    if formated_list[-1] in operators:
        display_error(f"\nError: expression cannot end with this operator : {formated_list[-1]}")
        return False

    for i in range(len(formated_list) - 1):
        a, b = formated_list[i], formated_list[i+1]

        # Two operators in a row, with special cases with negative - and ( ) 
        if a in operators and b in operators:
            if b == "-" and i+2 < len(formated_list) and (is_valid_number(formated_list[i+2]) or formated_list[i+2] == "("):
                continue
            display_error("\nError: two operators in a row.")
            return False

        # Parentheses syntax errors 
        if a == "(" and b == ")":
            display_error("\nError: empty parentheses.")
            return False

        if a == "(" and b in operators - {"-"}:
            display_error("\nError: operator after '('.")
            return False

        if a in operators and b == ")":
            display_error("\nError: operator before ')'")
            return False
        
        if is_valid_number(a) and b == "(":
            display_error("\nError: missing operator before '('.")
            return False
        
        if a == ")" and is_valid_number(b):
            display_error("\nError: missing operator after ')'.")
            return False
        
        if is_valid_number(a) and is_valid_number(b):
            display_error("\nError: missing operator between numbers.")
            return False

        # Number errors
        if a not in operators and a not in ["(", ")"] and not is_valid_number(a):
            display_error(f"\nError: invalid number: {a}")
            return False
        if b not in operators and b not in ["(", ")"] and not is_valid_number(b):
            display_error(f"\nError: invalid number: {b}")
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
    return float(left) ** float(right)

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

    # find deepest parenthesis
    while ")" in expression_list : 
        for i in range(len(expression_list)) : 
            if expression_list[i] == ")" : 
                closing_parenthesis_index = i 
                break
        
        opening_parenthesis_index = find_matching_open(expression_list, closing_parenthesis_index)

        # extract what's inside it
        inside_parenthesis = expression_list[opening_parenthesis_index + 1 : closing_parenthesis_index]

        # replace it with its value 
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
            if result == 0:
                result = 0
            print(f"\nResult: {result}\n")

            history.append({"expression": checked_expression, "result": result})
            json_management.save_history(history)

            input("Press Enter to continue...")
            return

        except ZeroDivisionError:
            display_error("\nError : division by 0 is not allowed.")
            continue
        except OverflowError:
            display_error("\nError : overflow, try smaller")
            continue

if __name__ == "__main__" :

    USE_GUI = False
    menu()

   
