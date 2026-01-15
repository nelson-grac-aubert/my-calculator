from tkinter import *
import calculator

calculator.USE_GUI = True

win=Tk()
win.title("Calculator")
win.geometry('560x580')
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

    expr = operator
    lst = calculator.format_string(expr)

    if not calculator.validate_list(lst):
        return  # L’erreur a déjà été affichée par display_error()

    try:
        lst = calculator.resolve_parenthesis(lst)
        result = calculator.calculate(lst)
        _input.set(result)
        operator = ""
    except ZeroDivisionError:
        calculator.display_error("Error: division by 0 is not allowed.")
    except OverflowError:
        calculator.display_error("\nError : overflow, try smaller")

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


bequal=Button(win,padx=14,pady=16,bd=5,width = 33, fg="black", font=('ariel', 16 ,'bold'),text="=",bg="grey",command=answer)
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


win.mainloop()
