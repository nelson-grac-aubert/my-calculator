from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Exemple")
root.geometry("300x150")

def message_error() :
    messagebox.showerror("Erreur", "Opération non executée")

boutton = Button(root, text="Declencher l'erreur", command=message_error)
boutton.pack(pady=20)

root.mainloop()