# **Robotic Bulk Messaging System**

The robotic bulk messaging system is a versitile application designed to streamline and automate WhatsApp messaging processes. It provides a convenient way to manage and send bulk messages to a target audience.

## **Key Features**

- **Google Sheets Integration**: Connects seamlessly with Google Sheets to fetch recipient data, making it easy to manage and organize contact information.

- **Customizable Message Templates**: Allows you to define and customize message templates according to your specific needs. Whether it's sending appointment reminders, sharing important updates, or promotional messages, you can tailor the content to suit your requirements.

- **File Attachment Support**: Attach files such as PDFs, images, or documents to your messages. This feature is particularly helpful for sending documents, flyers, or any other relevant files.

- **Scheduled Messaging**: Set a specific time for your messages to be sent and let the bot do the job. This enables you to plan your messaging campaigns in advance and ensures timely delivery.

- **Browser Automation**: Utilizes Selenium and ChromeDriver to automate web browser actions. It navigates to WhatsApp Web, logging in using your browser profile, and sends messages on your behalf.

- **Cross-Industry Applicability**: While initially developed for a nutritionist office, the script was built in a way that allows it to be applied to various fields. Whether you're in healthcare, customer service, marketing, or any other industry that requires bulk messaging, this application can be customized to suit your specific needs.

## **Usage**

When started, the system opens a window with the **main menu**:

![window](readme_images\main_menu.png)

- **Ver planilha** (*See worksheet*): opens the spreadsheet on the browser: ![window](readme_images\see_worksheet.png)
- **Editar mensagens** (*Edit messages*): section to edit messages, in the specific use case there were 7 possible types of message (*image 1*), where two of them included the possibility for file addition (*image 2*). When editing message texts, the texts configurations, such as row breaks or font weight changes (\*\*, ~~, __) are saved (*image 3*).

|![window](readme_images\edit_messages.png)|![window](readme_images\file_or_message.png)|![window](readme_images\edit_message.png)|
|-|-|-|

For files (*Arquivo*) the user can select a pdf or image file:

![window](readme_images\file_nofile.png)
![window](readme_images\file_addedfile.png)

When editing either texts or files, they need to be saved by clicking on "**Salvar**" (*Save*) button

- **Ativar robô** (*Activate robot*): opens a window with a clock and a timer, counting down to the next ocurrence of the time on the clock. When the countdown is over, it runs the process to send messages and restarts the countdown.

![window](readme_images\clock_9am.png)
![window](readme_images\clock_330pm.png)

- **Enviar mensagens para Pacientes** or **para Contatos** (*Send messages to ... or ...*): runs the process to send messages to the specified Sheet from the Worksheet. The process for both is as follows:
1. Check which users should receive which messages
2. Opens Whatsapp Web with each one's numbers and corresponding message model, substituting the variables with data from the worksheet:
![window](readme_images\apiwhats.png)
3. Attach file, if there is one
4. Click to send message

After this process is done from these buttons, the user receives a sucessful message box confirmation.

- **Sair** (*Leave*): Closes the window

## **System Requirements**

The system requires setting up Google Sheets API integration, installing Selenium Basic and updating its Chrome Driver executable to the correct version. It also requires the user to be previously logged in on Whatsapp Web on their browser.

1. Download and install [Selenium Basic](https://github.com/florentbr/SeleniumBasic/releases/download/v2.0.9.0/SeleniumBasic-2.0.9.0.exe) from [this repository](https://github.com/florentbr/SeleniumBasic/releases)
2. Download the appropriate [Chrome Driver](https://chromedriver.chromium.org/downloads) version according to [browser version](chrome://settings/help)
3. Move Chrome Driver executable from the downloaded zip to SeleniumBasic folder, created on its installation. It is normally located at **C:\Users\\<CURRENT-USER\>\AppData\Local\SeleniumBasic**
4. Set up the Google Sheets API and obtain the ***credentials.json*** file according to [this](https://developers.google.com/sheets/api/quickstart/python#enable_the_api)
5. For developers, the script requires **Python>=3.7** and the modules in **requirements.txt**
6. For clients, the script is bundled in an executable with [PyInstaller](https://pyinstaller.org/en/stable/), which generates a dist folder with the necessary files to run the script without installing Python or any of the modules on the user's computer:
```
python -m PyInstaller -n "Name for the App" --add-data="message_models.json;." --add-data="credentials.json;." --add-data="images;images" --add-data="Files;Files" --icon=images/ms-icon-70x70.ico --noconfirm --noconsole main.py
```
- **python -m PyInstaller**: runs the PyInstaller bundler
- **-n "Name for the App"**: defines the name that'll be used to identify the folder and the executable created inside *dist* folder
- **--add-data="\<origin\>;\<destination\>"**: defines the data that needs to be included in the bundle: the JSONs for the credentials and message_models, which are copied to the bundle root folder and images and Files folders are copied entirely
- **--icon="\<app_icon.ico\>"**: defines the icon image used for the executable created. **It MUST be in *.ico* format**
- **--nocofirm**: when running PyInstaller for the second time on, the module will ask to confirm the current *dist* folder overwriting. This flag is used to avoid the question and automatically overwrite the folder and inner files
- **--noconsole**: defines that no command prompt window is opened when the executable is started
- **main.py**: the system's entry python file
7. Log in on [WhatsApp Web](https://web.whatsapp.com/) for the chosen browser profile

## **Source Code**
### **message_models.json**
A JSON file containing all the message models established with the client, including file paths:
```
{
  "PACIENTES": {
    "CONSULTA": "Olá {{nome}}! Bom dia, tudo bem? \nEstou entrando em contato para confirmar a sua consulta de acompanhamento nutricional agendada para {{data}} às {{horario}}.",
    "CORTESIA": "",
    "PLANTAO": "",
    "MISSOES": "",
    "DICAS": {
      "file": "",
      "text": ""
    },
    "FEEDBACK": ""
  },
  "CONTATOS": {
    "file": "",
    "text": ""
  }
}
```
### **main.py**
The system entries on **main.py**, the code was planned to have two possibilities of execution: either with and argument indicating it should only run the script to send messages or without arguments to open the main menu window:
```
...
def main():
    if len(sys.argv) == 1:
        Window()

    else:
        send_messages()
...
```

### **models.py**
This file includes the Message class, used to retrieve the appropriate text and, if so, image path from the message_models file. It also includes the exportable functions to retrieve and edit message_models
```
...
# Models variable
models = {}

# Set models
with codecs.open('message_models.json', 'r', encoding="utf-8") as file:
    models = json.load(file)

# Messages Model 
class Message:

    # Get a message model
    def __init__(self, type, **user_data):
        ...

# Get models function
def get_model(type = None):

    global models

    with codecs.open('message_models.json', 'r', encoding="utf-8") as file:
        models = json.load(file)

    ...

# Edit models function
def edit_model(model, **model_data):
    # Get models
    with codecs.open('message_models.json', "r", encoding="utf-8") as file:
        models = json.load(file)
    
    ...

    # Overwrite models
    with codecs.open('message_models.json', 'w', encoding="utf-8") as file:
        json.dump(models, file, indent = 2, ensure_ascii=False)
    ...
```

### **windows.py**
Create and manage tkinter windows. Includes the Window class, used to create the tkinter root used by the system, it includes the specifications of design, text contents for components, images setups and all of the window's behavior management. It also includes a exportable function that shows the appropriate tkinter *messagebox* according to an argument.
```
...
class Window:
    def __init__(self):
        
        # Start window
        self.root = Tk()

        # Window title
        self.root.title("Sistema de Disparo de Mensagens - Raynara Santos")

        # Window background color
        self.root.config(background = "#2f0f07")
        ...
    ...

    # Function to set the main menu
    def main_menu(self):
        
        # Clean up window and set up logo
        self.clear_window()
        self.set_logo()

        # See worksheet button
        see_worksheet = ttk.Button(self.root, text="Ver planilha", command=self.open_worksheet)
        see_worksheet.pack()
        ...
    ...

# Message box function
def message_box(type, title, message):
        
    # If warning
    if type == 'warning':
        messagebox.showwarning(title, message)

    # If error
    elif type == 'error':
        messagebox.showerror(title, message)

    # If info
    else:
        messagebox.showinfo(title, message)
```

### **script.py**
Includes all of the browser's manipulation and Google Sheets API integrations and handling. It includes exportable functions that shall be mentioned particularly.
```
...
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = "1QyxUDa039jEmNGHZXCWcjh6eZ0srBN6Dz_QOuCMhyoA" 
PACIENTES_RANGE = 'Pacientes!A2:H'
CONTATOS_RANGE = 'Contatos!A2:C'
...
```
> ***start_driver():*** This function is used to start a Chrome Driver instance and return it. It uses the determined *User Data* folder to open the browser, if the browser is already in use if runs an exception to warn the user to close the browser and try again.
```
...
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
...
```

>***retry(action):*** This function is used to retry browser actions every 5 seconds if they fail until they succeed.
```
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
```

>***send_messages(sheet = None):*** This function includes all of credentials manipulation to read the data from the spreadsheet, managing the data though a *Pandas* dataframe, doing that for each type of message and then sending the message for each row of the chosen sheet or both if none is chosen.
```
...
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
        ...
        
        # List of dataframes
        lists = [consultas, cortesias, plantao, missoes, dicas, feedback]

        # For each item in lists
        for item in range(len(lists)):
            ...

            # For each row in each list
            for index, each in lists[item].iterrows():
                
                # Set person's name
                nome = each['Nome'].split(" ")[0]

                # Set person's phone
                phone = each['Telefone']
                ...

                # Start chrome driver
                chrome = start_driver()

                # Open url
                chrome.get(url)

                # Click action button to open conversation
                retry(lambda: chrome.find_element(By.XPATH, '//*[@id="action-button"]').click())

                # Click link to web whatsapp
                retry(lambda: chrome.find_element(By.XPATH, '//*[@id="fallback_block"]/div/div/h4[2]/a').click())
                ...

    def contacts_messages():
            
        # Get Contatos worksheet
        contacts_worksheet = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=CONTATOS_RANGE).execute()
        
        # Get contacts data
        contacts_data = contacts_worksheet.get('values', [])
        ...

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
    ...
```

## **Credits**
Software planning, designing and development: [Myself](https://github.com/Takater)

Client: [Raynara Santos Nutricionista](https://www.instagram.com/ray.nutricionista/)