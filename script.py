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
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.common.exceptions import WebDriverException

from models import Message
from datetime import datetime, timedelta

import urllib.parse
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
        DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

        # Connect to Google Sheets
        service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)

        # Retrieve all spreadsheets
        sheets = service.spreadsheets()

        # Send messages to patients
        def patients_messages():

            # Get Pacientes worksheet
            patients_worksheet = sheets.values().get(
            spreadsheetId = SPREADSHEET_ID,
            range = PACIENTES_RANGE).execute()

            # Get patients data values
            patients_data = patients_worksheet.get('values', [])

            # If no patients
            if not patients_data:

                # Return message box if opened from window
                if sheet:
                    return message_box("info", "Planilha sem dados", "Nenhum dado encontrado na planilha")
                
                # Return not found code
                return 404
            
            # Function to check if date is any of the specified days away from today
            def days_away(date_tuple, days):
                 
                 # Safety check
                 if date_tuple:

                    # Get date from tuple
                    consulta_date = date_tuple[0]

                    # Get each day away from days to today's date
                    days_away = [datetime.now().date() + timedelta(days=day) for day in days]

                    # Return if date from tuple is in days away from today
                    return consulta_date.date() in days_away

            # Set datetimes for row
            def set_datetimes(row_str):    
                    
                    # Safety check
                    if row_str:

                        # Set variables from string
                        date_str, time_str = row_str.split(", ")

                        # Set date from date string
                        date = datetime.strptime(date_str, "%d/%m/%Y")

                        # Set tuple with date and time string
                        return (date, time_str)
            
            # Set Dataframe from worksheet
            patients_table = pd.DataFrame(patients_data, columns=['Nome', 'Telefone', 'Consulta', 'Cortesia', 'Plantão', 'Missões', 'Dicas', '1ª Consulta'])

            # Get non empty rows
            patients_table = patients_table[patients_table["Nome"] != '']
            
            # Set rows with non empty "Consulta" column
            consultas = patients_table[patients_table["Consulta"] != '']

            # Set date string to datetime 
            consultas["Consulta"] = consultas["Consulta"].apply(set_datetimes)

            # Get rows where date is within limit
            consultas = consultas[
                consultas["Consulta"].apply(
                
                # Call function for each row for 1 or 5 days away
                lambda row: days_away(row, [1, 5])
            )]
            
            # Get name, phone and appointment date columns
            consultas = consultas[["Nome", "Telefone", "Consulta"]]

            # Set with non empty complimentary appointments
            cortesias = patients_table[patients_table["Cortesia"] != '']

            # Set date string to datetime
            cortesias["Cortesia"] = cortesias["Cortesia"].apply(set_datetimes)

            # Get rows where date is within limit
            cortesias = cortesias[
                cortesias["Cortesia"].apply(
                
                # Call function for each row for 1 day away
                lambda row: days_away(row, [1])
            )]
            
            try:
                # Get name, phone and complimentary appointment date columns
                cortesias = cortesias[["Nome", "Telefone", "Cortesia"]]
            except KeyError:
                pass

            # Set table for checked in duty
            plantao = patients_table[patients_table["Plantão"].apply(lambda value: value == 'TRUE')][["Nome", "Telefone"]]

            # Set table for checked in mission
            missoes = patients_table[patients_table["Missões"].apply(lambda value: value == 'TRUE')][["Nome", "Telefone"]]
            
            # Set table for checked in tips
            dicas = patients_table[patients_table["Dicas"].apply(lambda value: value == 'TRUE')][["Nome", "Telefone"]]

            # Set table for checked in feedback
            feedback = patients_table[(patients_table["Consulta"] != '') & (patients_table["1ª Consulta"].apply(lambda value: value == 'TRUE'))]
            feedback["Consulta"] = feedback["Consulta"].apply(set_datetimes)
            feedback = feedback[feedback["Consulta"].apply(
                
                # Call function for each row for 1 day before
                lambda row: days_away(row, [-1])

            )]

            # Get name and phone
            feedback = feedback[["Nome", "Telefone", "Consulta"]]

            # List of dataframes
            lists = [consultas, cortesias, plantao, missoes, dicas, feedback]

            # For each item in lists
            for item in range(len(lists)):
                
                # Check if list is not empty
                if len(lists[item]) > 0:
                    
                    # For each row in each list
                    for index, each in lists[item].iterrows():
                        
                        # Set person's name
                        nome = each['Nome'].split(" ")[0]

                        # Set person's phone
                        phone = each['Telefone']

                        # Start type and message variables
                        type_message = ''
                        message = None

                        # If list is Consultas or Cortesias
                        if item in [0, 1]:

                            # Set days of the week list
                            weekdays = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

                            # Start date and hour variables
                            data = None
                            horario = ''

                            # If list is Consultas
                            if item == 0:
                                
                                # Set message type
                                type_message = 'CONFIRMAR CONSULTA'

                                # Set day of the week
                                day_of_the_week = weekdays[int(each['Consulta'][0].strftime("%w"))]

                                # Set date with day of the week and hour variables
                                data, horario = f"{each['Consulta'][0].strftime('%d/%m/%Y')} - {day_of_the_week}", each['Consulta'][1]

                            # If list is Cortesias
                            elif item == 1:

                                # Set message type
                                type_message = 'CONFIRMAR CORTESIA'

                                # Set day of the week
                                day_of_the_week = weekdays[int(each['Cortesia'][0].strftime("%w"))]

                                # Set date with day of the week and hour variables
                                data, horario = f"{each['Cortesia'][0].strftime('%d/%m/%Y')} - {day_of_the_week}", each['Cortesia'][1]

                            # Set message data
                            message = Message(type_message, name=nome, date=data, hour=horario)

                        # If list is Plantao, Missoes, Dicas or Feedback
                        else:

                            # Set message type
                            type_message = 'PLANTAO' if item == 2 else (
                                'MISSOES' if item == 3 else (
                                'DICAS' if item == 4 else 'FEEDBACK'
                                )
                            )
                            
                            # Set message data
                            message = Message(type_message, name=nome)

                            if message.message == '':
                                break

                        # Open url with appropriate data
                        url = "https://api.whatsapp.com/send?phone=55" + phone + "&text=" + urllib.parse.quote(message.message)

                        # Start chrome driver
                        chrome = start_driver()

                        # Open url
                        chrome.get(url)

                        # Click action button to open conversation
                        retry(lambda: chrome.find_element(By.XPATH, '//*[@id="action-button"]').click())

                        # Click link to web whatsapp
                        retry(lambda: chrome.find_element(By.XPATH, '//*[@id="fallback_block"]/div/div/h4[2]/a').click())

                        # If message might have file
                        if type_message == 'DICAS':

                            # Get file path
                            file = message.image

                            # Start file input xpath variable
                            file_input = ''

                            # Click Clip button
                            retry(lambda: chrome.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span').click())

                            # If file is pdf
                            if file[-3:] == 'pdf':

                                # Set file input xpath
                                file_input = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[4]/button/input'

                            # If file is image
                            else:
                                
                                # Set image input xpath
                                file_input = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'
                            
                            # Send file path to input
                            retry(lambda: chrome.find_element(By.XPATH, file_input).send_keys(file))

                            # Click send button
                            retry(lambda: chrome.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span').click())
                        else:
                            # Click button so send message
                            retry(lambda: chrome.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click())

                        # Wait 10 seconds before leaving
                        time.sleep(10)

                        chrome.quit()
            
            return 200
            
        def contacts_messages():
            
            # Get Contatos worksheet
            contacts_worksheet = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=CONTATOS_RANGE).execute()
            
            # Get contacts data
            contacts_data = contacts_worksheet.get('values', [])

            # If no data is found
            if not contacts_data:

                # If coming from window
                if sheet:
                    
                    # Return message box to user
                    return message_box("info", "Planilha sem dados", "Nenhum dado encontrado na planilha")
                
                # Return error code
                return 404
            
            # Set dataframe from contacts data
            contacts_table = pd.DataFrame(contacts_data, columns=['Nome', 'Telefone', 'Enviar'])

            # Get non-empty name-field rows
            contacts_table = contacts_table[contacts_table['Nome'] != '']

            # Get contacts supposed to send
            contacts_table = contacts_table[contacts_table['Enviar'].apply(lambda value: value == 'TRUE')]

            # Get name and phone
            contacts_table = contacts_table[['Nome', 'Telefone']]

            # For each row in dataframe
            for index, each in contacts_table.iterrows():

                # Get first name
                nome = each['Nome'].split()[0]

                # Get phone
                phone = each['Telefone']

                # Set message
                message = Message('CONTATOS', name=nome)

                # If no message is set, skip
                if message.message == '':
                    break
                
                # Set url with data
                url = "https://api.whatsapp.com/send?phone=55" + phone + "&text=" + urllib.parse.quote(message.message)

                # Start chrome driver
                chrome = start_driver()

                # Open url
                chrome.get(url)

                # Click action button to open conversation
                retry(lambda: chrome.find_element(By.XPATH, '//*[@id="action-button"]').click())

                # Click link to web whatsapp
                retry(lambda: chrome.find_element(By.XPATH, '//*[@id="fallback_block"]/div/div/h4[2]/a').click())
                
                # Get file path
                file = message.image

                # If there's any file set
                if file:

                    # Start file input xpath variable
                    file_input = ''

                    # Click Clip button
                    retry(lambda: chrome.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span').click())

                    # If file is pdf
                    if file[-3:] == 'pdf':

                        # Set file input xpath
                        file_input = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[4]/button/input'

                    # If file is image
                    else:
                        
                        # Set image input xpath
                        file_input = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'

                    # Send file path to input
                    retry(lambda: chrome.find_element(By.XPATH, file_input).send_keys(file))
                    
                    # Click send button
                    retry(lambda: chrome.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span').click())
                
                # If no file set
                else:
                    
                    # Click button to send message
                    retry(lambda: chrome.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click())

                # Close browser
                chrome.quit()

            # Return success code
            return 200

        # Send messages
        if sheet:

            # If sheet, run only one of functions
            if sheet == 'Pacientes':
                return patients_messages()
            
            if sheet == 'Contatos':
                return contacts_messages()
            
        # Else, run both
        else:
            return [patients_messages(), contacts_messages()]

    except HttpError as err:
        return message_box("error", "Erro", err) if sheet else print(err)

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
        options.add_argument('--profile-directory=Profile 1')

        # Don't close browser window automatically
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

# Retry function
def retry(action):
    
    # Set success to false
    success = False

    # While success is false
    while not success:

        # Try action
        try:

            # Action
            action()

            # Wait 1 second before leaving
            time.sleep(1)

            # If no exception, success is set to True
            success = True
        
        # If action fail
        except:

            # Wait 5 seconds before continue
            time.sleep(5)

            # Next loop iteration
            continue