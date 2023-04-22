import os, time

from script import send_messages, start_driver, message_box,SPREADSHEET_ID

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
        photo = ImageTk.PhotoImage(image.resize((300, 150), Image.ANTIALIAS))

        logo = Label(self.root, image=photo, background="#2f0f07")
        logo.pack()
        
        # Set style
        style = ttk.Style()
        style.configure(".", font=("Arial", 18))
        style.theme_use('alt')
        style.configure("TButton", background='#2f0f07', padding = "30 10 30 10", foreground="#ccc", borderwidth="0", font=("Arial", 12))
        style.map('TButton', background=[('active', '#280700')], foreground=[('active', '#eab676')])

        # Open Main menu
        self.main_menu()

        # Run window
        self.root.mainloop()
        return


    def main_menu(self):


        see_worksheet = ttk.Button(self.root, text="Ver planilha", command=self.open_worksheet)
        see_worksheet.pack()
        
        edit_messages = ttk.Button(self.root, text="Editar mensagens", command=self.edit_messages)
        edit_messages.pack()

        patients_messages = ttk.Button(self.root, text="Enviar mensagens para Pacientes", command=lambda: self.messages(sheet='Pacientes'))
        patients_messages.pack()

        contacts_messages = ttk.Button(self.root, text="Enviar mensagens para Contatos", command=lambda: self.messages(sheet='Contatos'))
        contacts_messages.pack()

        quit_button = ttk.Button(self.root, text="Sair", command=lambda: self.root.quit())
        quit_button.pack()


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

        label = ttk.Label(self.root, text=f"Enviando mensagens \npara {sheet}...", font=('Arial', 32), background="#2f0f07", foreground="#ccc", padding="30 50 30 0")
        label.pack()

        result = send_messages(sheet)

        if result:
            if type(result) == int:
                if result == 200:
                    message_box("info", "Resultados de Envio", f"Mensagens enviadas para {sheet} com sucesso.")
            else:
                result()

        self.clear_window()
        self.main_menu()
        
        return

    def clear_window(self):
         
         # Destroy all widgets
        for item in self.root.winfo_children():
            item.destroy()

        return