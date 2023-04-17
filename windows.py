import os, time

from script import send_messages, start_driver, SPREADSHEET_ID

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Window:
    def __init__(self):
        
        # Start window
        self.root = Tk()

        self.root.title("Sistema de Disparo de Mensagens - Raynara Santos")

        self.root.geometry("600x400")
        self.root.config(background = "#2f0f07")

        image = Image.open("./raynara-logo.png")
        photo = ImageTk.PhotoImage(image)

        logo = Label(self.root, image=photo, background="#2f0f07", height=250)
        logo.pack()
        
        # Set style
        style = ttk.Style()
        style.configure(".", pady=100, padx=20, font=("Arial", 18))

        # Open Main menu
        self.main_menu()

        # Run window
        self.root.mainloop()
        return


    def main_menu(self):


        see_worksheet = ttk.Button(self.root, text="Ver planilha", command=self.open_worksheet)
        see_worksheet.pack()
        
        patients_messages = ttk.Button(self.root, text="Enviar mensagens para Pacientes", command=lambda: self.messages(sheet='Pacientes'))
        patients_messages.pack()

        contacts_messages = ttk.Button(self.root, text="Enviar mensagens para Contatos", command=lambda: self.messages(sheet='Contatos'))
        contacts_messages.pack()

        edit_messages = ttk.Button(self.root, text="Editar mensagens", command=self.edit_messages)
        edit_messages.pack()

        return
        
    def open_worksheet(self):

            # Start chrome driver
            chrome = start_driver()

            # Open worksheet
            chrome.get(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

            input()

    def edit_messages():
        ""
        return

    def messages(self, sheet):
        
        # Clear window
        self.clear_window()

        label = ttk.Label(self.root, text=f"Enviando mensagens para {sheet}...", font=('Arial', 12))
        label.pack()

        send_messages(sheet)

        return

    def clear_window(self):
         
         # Destroy all widgets
        for item in self.root.winfo_children():
            item.destroy()

        return