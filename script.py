from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.common.exceptions import WebDriverException

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.common.exceptions import WebDriverException

from models import Message
from urllib.parse import quote as url_parse
from datetime import datetime, timedelta

import time, os, sys, math, pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = "1QyxUDa039jEmNGHZXCWcjh6eZ0srBN6Dz_QOuCMhyoA" 
PACIENTES_RANGE = 'Pacientes!A2:H'
CONTATOS_RANGE = 'Contatos!A2:C'

def send_messages(sheet = None):
        
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
        sheets = service.spreadsheets()

        def patients_messages():

            patients_worksheet = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=PACIENTES_RANGE).execute()

            patients_data = patients_worksheet.get('values', [])

            if not patients_data:
                 message_box("info", "Planilha sem dados", "Nenhum dado encontrado na planilha")
                 return
            
            def one_day_away(date_tuple):
                 if date_tuple:
                    consulta_date = date_tuple[0]
                    one_day_away = datetime.now().date() + timedelta(days=1)
                    return consulta_date.date() == one_day_away

            # Set datetimes for row
            def set_datetimes(row_str):    
                    if row_str:
                        date_str, time_str = row_str.split(", ")
                        date = datetime.strptime(date_str, "%d/%m/%Y")
                        return (date, time_str)
            
            patients_table = pd.DataFrame(patients_data)

            patients_table["Consulta"] = patients_table["Consulta"].apply(set_datetimes)
            patients_table["Cortesia"] = patients_table["Cortesia"].apply(set_datetimes)
            
            consultas = patients_table[patients_table["Consulta"].apply(one_day_away)]

            cortesias = patients_table[patients_table["Cortesia"].apply(one_day_away)]

            plantao = patients_table[patients_table["Plantão"].apply(lambda value: value == 'TRUE')]

            missoes = patients_table[patients_table["Missões"].apply(lambda value: value == 'TRUE')]

            dicas = patients_table[patients_table["Dicas"].apply(lambda value: value == 'TRUE')]

            feedback = patients_table[patients_table["1ª Consulta"].apply(lambda value: value == 'TRUE')]

            for list in [consultas, cortesias, plantao, missoes, dicas, feedback]:
                for each in list:
                      
                    nome = each['Nome']
                    phone = each['Telefone']
                    type_message = ''
                    message = None

                    if list in [consultas, cortesias]:
                        data = None
                        horario = ''

                        if list is consultas:
                            type_message = 'CONFIRMAR CONSULTA'
                            data, horario = each['Consulta'][0], each['Consulta'][1]

                        elif list is cortesias:
                            type_message = 'CONFIRMAR CORTESIA'
                            data, horario, each['Cortesia'][0], each['Cortesia'][1]
                 
                        message = Message(type_message, name=nome, date=data, hour=horario)

                    else:
                        type_message = 'PLANTAO' if list is plantao else (
                            'MISSOES' if list is missoes else (
                            'DICAS' if list is dicas else 'FEEDBACK'
                            )
                        )
                        
                        message = Message(type_message, name=nome)

                    url = "https://api.whatsapp.com/send?phone=55" + phone + "&text=" + url_parse(message)

                    chrome = start_driver()

                    chrome.get(url)

                    time.sleep(20)

                    chrome.quit()

            

            
            

        def contacts_messages():
             "Send messages to contacts"

    except HttpError as err:
        print(err)

def message_box(type, title, message):
        
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

def start_driver():

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

            message_box("warning", "Navegador em uso", "Por favor, feche o navegador e tente novamente.")

            # Log exception and return
            print("Finalizado por navegador em uso")
            return


# Main function
def main ():

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of the spreadsheet.
    SPREADSHEET_ID = "1QyxUDa039jEmNGHZXCWcjh6eZ0srBN6Dz_QOuCMhyoA" 
    PACIENTES_RANGE = 'Pacientes!A2:H'
    CONTATOS_RANGE = 'Contatos!A2:C'
    

    """creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheets = service.spreadsheets()
        
        # Retrieve patients data
        patients_data = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=PACIENTES_RANGE).execute()
        
        # Get data from worksheet
        patients = patients_data.get('values', [])

        # If no data
        if not patients:
            print('Nenhum dado encontrado.')
            return

        # Variable if data has Dicas
        hasTips = False

        # Set hasTips to True if necessary
        for each in patients:
            if not each[0]:
                continue
            try:
                if each[6] == "TRUE":
                    hasTips = True
                else:
                    continue
            except IndexError:
                continue

        print(hasTips)

        window = Window()

        window.alert_window()

        # For each patient in found data
        for patient in patients:

            if not patient[0]:
                continue
            # Get name
            name = patient[0]

            # Get phone number
            phone = patient[1]

            # Check dates columns
            for col in range(2, 7):

                # Try if date is not empty
                try:

                    # Start date string variable
                    date_string = ''

                    # If col has date and time
                    if col in [2, 3]:
                        
                        # Get date and time
                        (date_string, hour) = patient[col].split(", ")

                    else:
                        # Get date string
                        date_string = patient[col]

                    if not date_string:
                        raise ValueError


                    # Format date
                    date = time.mktime(
                            datetime.strptime(
                                date_string, "%d/%m/%Y"
                            ).timetuple()
                        )

                    # Get Today
                    today = time.mktime(
                                datetime.now().timetuple()
                            )

                    # Get difference in days
                    diff = math.ceil((date - today) / (84600))

                except (IndexError, ValueError):
                    continue    
            
    except HttpError as err:
        print(err)"""

# Run main when executed
if __name__ == "__main__":
    main()