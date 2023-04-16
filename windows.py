import os, time

from tkinter import *
from tkinter import ttk

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.common.exceptions import WebDriverException

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = "1QyxUDa039jEmNGHZXCWcjh6eZ0srBN6Dz_QOuCMhyoA" 
PACIENTES_RANGE = 'Pacientes!A2:H'
CONTATOS_RANGE = 'Contatos!A2:C'

class Window:
    def __init__(self):
        
        # Start window
        self.root = Tk()
        
        # Set style
        style = ttk.Style()
        style.configure(".", pady=100, padx=20, font=("Arial", 18))

        # Open Main menu
        self.main_menu()

        # Google Sheets Credentials variable
        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Connect to Google Sheets
            service = build('sheets', 'v4', credentials=creds)

            # Retrieve all spreadsheets
            self.sheets = service.spreadsheets()

        except HttpError as err:
            print(err)

        # Run window
        self.root.mainloop()
        return


    def main_menu(self):


        see_worksheet = ttk.Button(self.root, text="Ver planilha", command=self.open_worksheet)
        see_worksheet.pack()
        
        patients_messages = ttk.Button(self.root, text="Enviar mensagens para Pacientes", command=lambda: self.send_messages(sheet='Pacientes'))
        patients_messages.pack()

        contacts_messages = ttk.Button(self.root, text="Enviar mensagens para Contatos", command=lambda: self.send_messages(sheet='Contatos'))
        contacts_messages.pack()

        edit_messages = ttk.Button(self.root, text="Editar mensagens", command=self.edit_messages)
        edit_messages.pack()

        return

    def start_driver(self):

        # Get user folder path
        user = os.environ["USERPROFILE"]

        # Get Chrome user data path
        chrome_data_dir = os.path.join(user, "AppData", "Local", "Google", "Chrome", "User Data")

        # Set options object
        options = webdriver.ChromeOptions()

        # Include user data folder path
        options.add_argument(f'--user-data-dir={chrome_data_dir}')

        # Set user profile path to Default
        options.add_argument('--profile-directory=Default')

        #
        options.add_argument('--detach')
        
        # Try to start driver
        try:
            # Open chrome with user profile
            driver = webdriver.Chrome(options=options)

            return driver

        # Exception for profile in use
        except WebDriverException:

            self.message_box("warning", "Navegador em uso", "Por favor, feche o navegador e tente novamente.")

            # Log exception and return
            print("Finalizado por navegador em uso")
            return
        
    def open_worksheet(self):

            # Start chrome driver
            chrome = self.start_driver()

            # Open worksheet
            chrome.get(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

            input()

    def edit_messages():
        ""
        return

    def send_messages(self, sheet):
        
        # Clear window
        self.clear_window()

        label = ttk.Label(self.root, text=f"Enviando mensagens para {sheet}...", font=('Arial', 12))
        label.pack()

        return


    def message_box(self, type, title, message):
        
        # Import messagebox
        from tkinter import messagebox
        
        # If warning
        if type == 'warning':
             messagebox.showwarning(title, message)

        # If error
        elif type == 'error':
             messagebox.showerror(title, message)

        # If info
        else:
             messagebox.showinfo(title, message)

    def clear_window(self):
         
         # Destroy all widgets
        for item in self.root.winfo_children():
            item.destroy()

        return