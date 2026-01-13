allowed_characters = '0123456789+-/*().%^ \n\r'
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
        if character=="/" and i+1<len(checked_string) and checked_string[i+1]=="/":
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

# def calculate(formated_list) : 
#     for i in range(len(formated_list)) : 
#         if formated_list[i] == "/" : 
#             left = formated_list[i-1] 
#             right = formated_list[i+1]
#             result = divide(left, right)

#         if formated_list[i] == "*" : 
#             left = formated_list[i-1] 
#             right = formated_list[i+1]
#             result = multiply(left, right)
    
#         if formated_list[i] == "+" : 
#             left = formated_list[i-1] 
#             right = formated_list[i+1]
#             result = add(left, right)
    
#         if formated_list[i] == "-" : 
#             left = formated_list[i-1] 
#             right = formated_list[i+1]
#             result = substract(left, right)


    # return result

def calculate(formated_list):
    list_without_power=[]
    i=0
    while i<len(formated_list):
        token=formated_list[i]
        match token:
            case "^":
                list_without_power[-1]=power(list_without_power[-1],formated_list[i+1])
                i+=2
                continue
            case _:
                list_without_power.append(token)
                i+=1
    list_without_div_mult=[]
    i=0
    while i<len(list_without_power):
        token=list_without_power[i]
        match token:
            case "*":
                list_without_div_mult[-1]=multiply(list_without_div_mult[-1],list_without_power[i+1])
                i+=2
                continue
            case "/":
                list_without_div_mult[-1]=divide(list_without_div_mult[-1],list_without_power[i+1])
                i+=2
                continue
            case "//":
                list_without_div_mult[-1]=divide_whole(list_without_div_mult[-1],list_without_power[i+1])
                i+=2
                continue
            case "%":
                list_without_div_mult[-1]=modulo(list_without_div_mult[-1],list_without_power[i+1])
                i+=2
                continue
            case _:
                list_without_div_mult.append(token)
                i+=1
    result=float(list_without_div_mult[0])
    i=1
    while i<len(list_without_div_mult):
        op=list_without_div_mult[i]
        right=list_without_div_mult[i+1]
        match op:
            case "+":
                result=add(result,right)
            case "-":
                result=substract(result,right)
        i+=2
    return result
        
def run_calculator():
    global history
    while running:
        checked_expression = check_characters(allowed_characters)
        expression_list = format_string(checked_expression)

        # dans le try on aura result = calculate(expression_list)
        # calculate() etant la fonction qui va gerer l'ordre des priorités et les parenthèses

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

    
        


