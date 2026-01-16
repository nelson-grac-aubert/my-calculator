from tkinter import *
import calculator
import json_management

calculator.USE_GUI = True
history = json_management.load_history()

win=Tk()
win.title("Calculator")
win.geometry('570x650')
win.configure(background='grey')


def  btnclick(num):
    global operator
    operator=operator + str(num)
    _input.set(operator)

def clear():
    global operator
    operator=""
    _input.set("")

def answer():
    global operator

    lst = calculator.format_string(operator)

    if not calculator.validate_list(lst):
        return  # L’erreur a déjà été affichée par display_error()

    try:
        lst = calculator.resolve_parenthesis(lst)
        result = calculator.calculate(lst)
        _input.set(result)

        history.append({"expression": operator, "result": result})
        json_management.save_history(history)
        operator = ""
    except ZeroDivisionError:
        calculator.display_error("Error: division by 0 is not allowed.")
    except OverflowError:
        calculator.display_error("\nError : overflow, try smaller")
    except (TypeError, IndexError, ValueError) : 
        calculator.display_error("\nError : invalid syntax")
    except Exception as e:
        # Last resort, in case all previous safeguards fail 
        calculator.display_error("\nError : unexpected error")

def clear_history():
    history.clear()
    json_management.save_history(history)

    
def view_history_window():
    global history
    operations_list = []
    for i, h in enumerate(history, 1):
        operations_list.append(f"{i}. {h['expression']} = {h['result']}")
    
    if not history:
            calculator.display_error("History is empty.")
    else:
        history_window = Toplevel(win)
        history_window.title("Calculation History")
        history_window.geometry("400x400")
        history_window.configure(background='lightgrey')

        history_text = Text(history_window, font=('ariel', 14), bg='white', wrap=WORD)
        history_text.pack(expand=True, fill=BOTH, padx=10, pady=10)

        history_text.delete(1.0, 'end')
        for item in operations_list:
            history_text.insert('end',item + '\n')

        label = Label(history_window, text="History", font=('ariel', 18, 'bold'), bg='lightgrey')
        label.pack(pady=10)

        history_text.config(state=DISABLED)

label=Label(win,font=('ariel' ,20,'bold'),text='Calculator',bg='grey',fg='black')
label.grid(columnspan=4)

_input=StringVar()
operator=""

display = Entry(win,font=('ariel' ,30,'bold'), textvariable=_input ,insertwidth=10 , bd=10 ,bg="white",justify='right')
display.grid(columnspan=4)

b7=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="7",bg="grey", command=lambda: btnclick(7) )
b7.grid(row=2,column=0)

b8=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="8",bg="grey", command=lambda: btnclick(8) )
b8.grid(row=2,column=1)

b9=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="9",bg="grey", command=lambda: btnclick(9) )
b9.grid(row=2,column=2)

Add=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 18 ,'bold'),text="+",bg="grey", command=lambda: btnclick("+") )
Add.grid(row=2,column=3)


b4=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="4",bg="grey", command=lambda: btnclick(4) )
b4.grid(row=3,column=0)

b5=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="5",bg="grey", command=lambda: btnclick(5) )
b5.grid(row=3,column=1)

b6=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="6",bg="grey", command=lambda: btnclick(6) )
b6.grid(row=3,column=2)

Sub=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="-",bg="grey", command=lambda: btnclick("-") )
Sub.grid(row=3,column=3)


b1=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="1",bg="grey", command=lambda: btnclick(1) )
b1.grid(row=4,column=0)

b2=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="2",bg="grey", command=lambda: btnclick(2) )
b2.grid(row=4,column=1)

b3=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="3",bg="grey", command=lambda: btnclick(3) )
b3.grid(row=4,column=2)

mul=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="*",bg="grey", command=lambda: btnclick("*") )
mul.grid(row=4,column=3)


b0=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 22 ,'bold'),text="0",bg="grey", command=lambda: btnclick(0) )
b0.grid(row=5,column=0)

bc=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 22 ,'bold'),text="c",bg="grey", command=clear)
bc.grid(row=5,column=1)

Decimal=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 24 ,'bold'),text=".",bg="grey", command=lambda: btnclick(".") )
Decimal.grid(row=5,column=2)

Div=Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 23 ,'bold'),text="/",bg="grey", command=lambda: btnclick("/") )
Div.grid(row=5,column=3)


bequal=Button(win,padx=25,pady=16,bd=5,width = 33, fg="black", font=('ariel', 16 ,'bold'),text="=",bg="grey",command=answer)
bequal.grid(columnspan=4)

Parenthèse_g =Button(win,padx=18,pady=16,bd=4, fg="black", font=('ariel', 21 ,'bold'),text="(",bg="grey", command=lambda: btnclick("(") )
Parenthèse_g.grid(row=5,column=5)

Parenthèse_d =Button(win,padx=18,pady=16,bd=4, fg="black", font=('ariel', 21 ,'bold'),text=")",bg="grey", command=lambda: btnclick(")") )
Parenthèse_d.grid(row=4,column=5)

Pourcentage =Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 18 ,'bold'),text="%",bg="grey", command=lambda: btnclick("%") )
Pourcentage.grid(row=3,column=5)

Puissance =Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="^",bg="grey", command=lambda: btnclick("^") )
Puissance.grid(row=2,column=5)

Div_d =Button(win,padx=16,pady=16,bd=4, fg="black", font=('ariel', 20 ,'bold'),text="//",bg="grey", command=lambda: btnclick("//") )
Div_d.grid(row=1,column=5)

View_h=Button(win,padx=1,pady=5,bd=5,width = 20, fg="black", font=('ariel', 16 ,'bold'),text="View History",bg="grey",command=view_history_window)
View_h.grid(column=2, columnspan=5)

Clear_h=Button(win,padx=1,pady=5,bd=5,width = 20, fg="black", font=('ariel', 16 ,'bold'),text="Clear History",bg="grey",command=clear_history)
Clear_h.grid(row=7, columnspan=2)


win.mainloop()




