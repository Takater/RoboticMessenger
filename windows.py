from tkinter import *
from tkinter import ttk

class Window:
    def __init__(self):
        self.root = Tk()

        btn = ttk.Button(text="Quit", command=self.root.destroy)
        btn.pack()

        self.root.mainloop()

    def alert_window(self):
        self.root.title("Alerta")
        self.root.geometry("300x300")