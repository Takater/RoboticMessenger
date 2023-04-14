from models import Message
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.common.exceptions import WebDriverException

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import time, os

# Main function
def main ():

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
    
    # Try to start driver
    try:
        # Open chrome with user profile
        chrome = webdriver.Chrome(options=options)



        # Start whatsapp
        chrome.get("https://web.whatsapp.com")

    # Exception for profile in use
    except WebDriverException:

        # Import ctypes module
        import ctypes

        # Message box for user
        ctypes.windll.user32.MessageBoxW(0, "Por favor, feche todas as janelas perfil Google Chrome.", "Perfil em uso", 48)

        # Log exception and return
        print("Finalizado por perfil em uso")
        return
    
    time.sleep(10)    

    chrome.quit()


# Run main when executed
if __name__ == "__main__":
    main()