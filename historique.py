import ast
import operator
import json
import os

allowed_characters = "0123456789+-*/().^ \n\r"
HISTORY_FILE = "history.json"
history = []

# opérateurs autorisés
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}


def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def safe_eval(expr):
    expr = expr.replace("^", "**")  # ^ → puissance
    node = ast.parse(expr, mode="eval").body
    return eval_node(node)


def eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        if type(node.op) not in OPERATORS:
            raise ValueError
        return OPERATORS[type(node.op)](
            eval_node(node.left),
            eval_node(node.right)
        )

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in OPERATORS:
            raise ValueError
        return OPERATORS[type(node.op)](
            eval_node(node.operand)
        )

    raise ValueError


def run_calculator():
    expression = input("Enter calculation: ")

    if not all(c in allowed_characters for c in expression):
        print("Invalid characters detected.")
        return

    try:
        result = safe_eval(expression)
        print(f"{expression} = {result}")

        history.append({
            "expression": expression,
            "result": result
        })
        save_history()

    except ZeroDivisionError:
        print("Error: division by zero")
    except Exception:
        print("Invalid expression")


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
            save_history()
            print("History cleared.")

        elif choice == "4":
            print("See you soon!")
            break

        else:
            print("Invalid choice")


# chargement automatique
load_history()
menu()
