from tkinter import *
from tkinter import ttk

class Window:
    def __init__(self):
        self.root = Tk()

    def alert_window(self):
        self.root.title("Alerta")
        self.root.geometry("300x100")