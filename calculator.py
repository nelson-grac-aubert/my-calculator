allowed_characters = '0123456789+-//*().%^ \n\r'
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
    while True:
        user_input = input("\nEnter your mathematical expression composed of only numbers and operators: ")

        invalid_found = False
        
        for character in user_input:
            if character not in allowed_characters:
                print("Allowed characters are digits 0-9 and operators + - / // * () % ^")
                invalid_found = True
                break 

        if not invalid_found:
            return user_input

def format_string(checked_string):
    input_turned_into_list=[]
    current_number=""
    i=0
    while i<len(checked_string):
        character=checked_string[i]
        if character in "0123456789.":
            current_number+=character
            i+=1
            continue
        if current_number!="":
            input_turned_into_list.append(current_number)
            current_number=""
        if character==" ":
            i+=1
            continue
        if character=="/" and i+1<len(checked_string) and checked_string[i+1]=="//":
            input_turned_into_list.append("//")
            i+=2
            continue
        input_turned_into_list.append(character)
        i+=1
    if current_number!="":
        input_turned_into_list.append(current_number)
    print(f"\nLa liste formatée sur laquelle on va faire les opérations : {input_turned_into_list}")
    return input_turned_into_list

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
    result=1
    for i in range(right):
        result=result*left
    return result

def pass_power(tokens):
    result = []
    i = 0

    while i < len(tokens):
        current_element = tokens[i]

        if current_element == "^":
            result[-1] = power(result[-1], tokens[i+1])
            i += 2
            continue

        result.append(current_element)
        i += 1

    return result

def pass_mult_div(tokens):
    result = []
    i = 0

    while i < len(tokens):
        current_element = tokens[i]
        match current_element:
            case "*":
                result[-1] = multiply(result[-1], tokens[i+1])
                i += 2
                continue
            case "/":
                result[-1] = divide(result[-1], tokens[i+1])
                i += 2
                continue
            case "//":
                result[-1] = divide_whole(result[-1], tokens[i+1])
                i += 2
                continue
            case "%":
                result[-1] = modulo(result[-1], tokens[i+1])
                i += 2
                continue
            case _:
                result.append(current_element)
                i += 1

    return result

def pass_add_sub(tokens):
    result = float(tokens[0])
    i = 1

    while i < len(tokens):
        operator = tokens[i]
        right = tokens[i+1]

        match operator:
            case "+":
                result = add(result, right)
            case "-":
                result = substract(result, right)

        i += 2

    return result

def calculate(tokens):
    tokens = pass_power(tokens)
    tokens = pass_mult_div(tokens)
    return pass_add_sub(tokens)
        
def run_calculator():
    global history
    while running:
        checked_expression = check_characters(allowed_characters)
        expression_list = format_string(checked_expression)

        try:
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