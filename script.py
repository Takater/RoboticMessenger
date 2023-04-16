from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.common.exceptions import WebDriverException

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models import Message
from windows import Window
from urllib.parse import quote as url_parse
from datetime import datetime

import time
import os
import math


# Main function
def main ():

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of the spreadsheet.
    SPREADSHEET_ID = "1QyxUDa039jEmNGHZXCWcjh6eZ0srBN6Dz_QOuCMhyoA" 
    PACIENTES_RANGE = 'Pacientes!A2:H'
    CONTATOS_RANGE = 'Contatos!A2:C'

    window = Window()
    

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