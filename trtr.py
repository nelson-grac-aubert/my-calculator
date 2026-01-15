from tkinter import *   

def create():
    win = Toplevel(root)

root = Tk()
root.geometry('200x100')  

btn = Button(root, text="Créer une nouvelle fenêtre", command = create)
btn.pack(pady = 10) 

root.mainloop()