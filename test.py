allowed_characters = "0123456789+-/*() "

def check_characters(expression):
    for character in expression:
        if character not in allowed_characters:
            return False
    return True


def calculator():
    while True:
        user_input = input(
            "\nEnter a mathematical expression"
            "(or 'q' for left) : "
        )

        if user_input.lower() == "q":
            print("See you soon")
            break

        if check_characters(user_input):
            try:
                result = eval(user_input)
                print("Result :", result)
            except ZeroDivisionError:
                print("Error : division by zero")
            except:
                print("Error in the expression ")
        else:
            print("Unauthorized characters! ")
            print("Allowed characters: numbers, + - * / ( )")


if __name__ == "__main__":
    calculator()




def calculatrice():
    historique = []

    while True:
        print("\n--- CALCULATRICE ---")
        print("1 - Nouveau calcul")
        print("2 - Voir l'historique")
        print("3 - Effacer l'historique")
        print("4 - Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            expression = input("Entrez une expression (ex: 3 + 5 * 2) : ")

