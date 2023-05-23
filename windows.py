import os, datetime, math

from script import send_messages, start_driver, SPREADSHEET_ID
from models import edit_model, get_model

from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class Window:
    def __init__(self):
        
        # Start window
        self.root = Tk()

        # Window title
        self.root.title("Sistema de Disparo de Mensagens - Raynara Santos")

        # Window background color
        self.root.config(background = "#2f0f07")

        # Open window maximized
        self.root.state('zoomed')
        
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

    # Function to set logo
    def set_logo(self):

        # Retrieve an adjust logo
        global photo
        image = Image.open("./images/raynara-logo.png")
        photo = ImageTk.PhotoImage(image.resize((300, 150), Image.ANTIALIAS))

        # Set logo in window
        logo = Label(self.root, image=photo, background="#2f0f07")
        logo.pack()

        return
    
    # Function to set robot logo
    def robot_logo(self):

        # Retrieve and adjust logo
        global photo
        image = Image.open("./images/robot.png")
        photo = ImageTk.PhotoImage(image.resize((150, 150), Image.ANTIALIAS))

        # Set logo in window
        logo = Label(self.root, image=photo, background="#2f0f07")
        logo.pack()

        return

    # Function to set the main menu
    def main_menu(self):
        
        # Clean up window and set up logo
        self.clear_window()
        self.set_logo()

        # See worksheet button
        see_worksheet = ttk.Button(self.root, text="Ver planilha", command=self.open_worksheet)
        see_worksheet.pack()
        
        # Edit messages button
        edit_messages = ttk.Button(self.root, text="Editar mensagens", command=self.edit_messages)
        edit_messages.pack()

        # Activate robot button
        turn_on_robot = ttk.Button(self.root, text="Ativar robô", command=self.activate_robot)
        turn_on_robot.pack()

        # Send messages to patients button
        patients_messages = ttk.Button(self.root, text="Enviar mensagens para Pacientes", command=lambda: self.messages(sheet='Pacientes'))
        patients_messages.pack()

        # Send messages to contacts button
        contacts_messages = ttk.Button(self.root, text="Enviar mensagens para Contatos", command=lambda: self.messages(sheet='Contatos'))
        contacts_messages.pack()

        # Quit button
        quit_button = ttk.Button(self.root, text="Sair", command=lambda: self.root.quit())
        quit_button.pack()

        return

    # Function to open worksheet        
    def open_worksheet(self):

            # Start chrome driver
            chrome = start_driver()

            # Open worksheet
            chrome.get(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

            # Don't close window
            input()
    
    # Activate robot
    def activate_robot(self):

        # Clear window and set up logo
        self.clear_window()
        self.robot_logo()

        # Countdown
        def update_countdown():

            # Variable to set countdown correctly
            hoursum = 0

            # Get time from time picker
            selected_time = time_picker.time()

            # 1pm to 11pm -> +12
            if selected_time[2] == 'PM' and selected_time[0] != 12:
                hoursum = 12

            # 1am to 11am -> +0
            elif selected_time[0] != 12:
                hoursum = 0
            
            # 12am and 12pm -> 0 or -12
            else:
                hoursum = 0 if selected_time[2] == 'PM' else -12

            # Set target time
            target_time = datetime.datetime.strptime((str(time_picker.time()[0] + hoursum) + ":" + str(time_picker.time()[1]) + ":" + "0"), "%H:%M:%S")

            # Time variables
            current_time = datetime.datetime.now()
            remaining_seconds = (target_time - current_time).seconds

            # Time is over
            if remaining_seconds <= 0:

                # Clear main label, set up countdown label and send messages
                main_label.destroy()
                countdown_label.config(text="Enviando mensagens")
                self.root.after(500, send_messages)
                self.activate_robot()
            
            # Update timer
            else:

                # Get remaining time parts
                rem_hours = math.floor(remaining_seconds/60/60)
                rem_minutes = math.floor(remaining_seconds/60) - (rem_hours * 60)
                rem_secs = math.floor((remaining_seconds/60 - math.floor(remaining_seconds/60)) * 60)

                # Set up remaining time string
                remaining_time = (
                    (str(rem_hours) if rem_hours > 9 else ("0" + str(rem_hours)))
                    + ":" + 
                    (str(rem_minutes) if rem_minutes > 9 else ("0" + str(rem_minutes)))
                    + ":" + 
                    (str(rem_secs) if rem_secs > 9 else ("0" + str(rem_secs)))
                )

                # Configure label
                countdown_label.config(text=remaining_time)

                # Rerun after 1 second
                self.root.after(1000, update_countdown)
        
        # Time picker
        from tktimepicker import AnalogPicker, AnalogThemes
        time_picker = AnalogPicker(self.root)
        AnalogThemes(time_picker).setNavyBlue()
        time_picker.setHours(9)
        time_picker.setMinutes(0)
        time_picker.pack()

        # Main label
        main_label = ttk.Label(self.root, font=("Arial", 14), foreground="#ccc", background="#2f0f07",padding="3 3 3 3", text="Próximo envio de mensagens ocorrerá em: ")
        main_label.pack()

        # Countdown label
        countdown_label = ttk.Label(self.root, font=("Arial", 24), foreground="#ccc", background="#2f0f07",padding="10 10 10 10", )
        countdown_label.pack()

        # Go back button
        goback = ttk.Button(self.root, text="Voltar", command=self.main_menu)
        goback.pack()

        # Run countdown updater
        update_countdown()
        

    # Edit message models or file paths
    def edit_messages(self):
        
        # Function to open text edition window
        def edit_message_model(chosen):

            current_model = get_model(chosen) if chosen not in ['Contatos', 'Dicas'] else get_model(chosen)['text']

            # Function to edit text model on JSON file and return result
            def save_button_click(model=str.upper(chosen)):

                # Get result from model edition
                result = edit_model(model, new_text=text.get("1.0", "end-1c"))

                # Successful result
                if result == 200:
                    message_box("info", "Mensagem de sucesso", f"O modelo para mensagem de {chosen} foi alterado com sucesso.")

                # Error result
                else:
                    message_box("error", "Mensagem de erro", f"Ocorreu um erro ao tentar editar o texto de {chosen}. Por favor, tente novamente ou contacte o administrador.")
                
                # Return to edit window
                self.edit_messages()
                    
            # Clear window and set logo
            self.clear_window()
            self.set_logo()

            # Label for chosen model
            label = ttk.Label(self.root, font=("Arial", 14), foreground="#ccc", background="#2f0f07",padding="10 10 10 10", text=f"Insira novo texto para {chosen}. Todas as configurações de texto serão preservadas.\nInsira variáveis entre chaves duplas {{{{ }}}}")
            label.pack()
            
            # Text input
            text = Text(self.root, width=80, height=10)
            text.pack()
            text.delete('1.0', END)
            text.insert('1.0', current_model)

            # Save button
            save_button = ttk.Button(self.root, text="Salvar", command=save_button_click)
            save_button.pack()

            # Go back button
            if chosen not in ['DICAS', 'CONTATOS']:
                
                # Go back to edit messages menu
                goback = ttk.Button(self.root, text="Voltar", command=self.edit_messages)
                goback.pack()
            else:

                # Go back to file or message menu
                goback = ttk.Button(self.root, text="Voltar", command=lambda: edit_file_or_message(chosen))
                goback.pack()

        # Function to open file path edition window
        def edit_file_path(chosen):

            # New path variable
            new_file_path = ''

            # Select file
            def select_file():
                
                # Reference global variable
                global new_file_path

                # Get file path
                path = filedialog.askopenfilename()
                
                # Selected path
                if path:

                    # Get file name
                    filename = os.path.basename(path)

                    # Set global path variable
                    new_file_path = path

                    file_path.config(text=f"Arquivo atual (clique para alterar): {filename}")

                    self.root.after(100, lambda: print("New file selected: %s", new_file_path))

                # No selected path
                else:
                    
                    # Warning message box
                    message_box("warning", "Mensagem de aviso", f"Nenhum arquivo selecionado para {chosen}")

            def delete_file():
                global new_file_path
                new_file_path = ''
                save_button_click()
            
            # Function to edit file path on JSON and return result
            def save_button_click(model=str.upper(chosen)):

                global new_file_path
                
                # Get result from model edition
                result = edit_model(model, new_file=new_file_path)

                # Successful result
                if result == 200:
                    message_box("info", "Mensagem de sucesso", f"O arquivo de imagem para {chosen} foi alterado com sucesso.")
                
                # Error result
                else:
                    message_box("error", "Mensagem de erro", f"Ocorreu um erro ao tentar alterar o arquivo para {chosen}. Por favor, tente novamente ou contacte o administrador.")
                
                # Return to edit window
                self.edit_messages()

            # Clear window and set logo
            self.clear_window()
            self.set_logo()

            # Label for chosen model 
            label = ttk.Label(self.root, font=("Arial", 12, "bold"), padding="10 10 10 10", foreground="#eab676", background="#2f0f07", text=f"Selecione novo arquivo para {chosen}.")
            label.pack()     

            # Current file name
            filename = os.path.basename(get_model(chosen)['file'])
            # File input
            file_path = ttk.Button(self.root, text=(

                    # Set button text 
                    "Clique aqui para selecionar arquivo" if not filename else f"Arquivo atual (clique para alterar): {filename}"
                
                # Command to open file dialog
                ), command=select_file)
            
            file_path.pack()

            if filename:
                close = ttk.Button(self.root, text="Excluir imagem", command=delete_file)
                close.pack()

            # Save button
            save_button = ttk.Button(self.root, text="Salvar", command=save_button_click)
            save_button.pack()

            # Go back button
            goback = ttk.Button(self.root, text="Voltar", command=lambda: edit_file_or_message(chosen))
            goback.pack()
        
        # Function to open file or message edition window
        def edit_file_or_message(model):
            
            # Clear window and set logo
            self.clear_window()    
            self.set_logo()

            # Label for chosen model
            label = ttk.Label(self.root, font=("Arial", 12, "bold"), padding="10 10 10 10", foreground="#eab676", background="#2f0f07", text=f"Atualizar {model}\n")
            label.pack()

            # Button to edit file path
            file_path_button = ttk.Button(self.root, text="Arquivo", command=lambda: edit_file_path(model))
            file_path_button.pack()

            # Button to edit message text
            message_model_button = ttk.Button(self.root, text=f"Texto da mensagem", command=lambda: edit_message_model(model))
            message_model_button.pack()

            # Go back button
            goback = ttk.Button(self.root, text="Voltar", command=self.edit_messages)
            goback.pack()
        
        # Clear window and set logo
        self.clear_window()
        self.set_logo()

        # Label for edit message window
        main_label = ttk.Label(self.root, font=("Arial", 12, "bold"), padding="10 10 10 10", foreground="#eab676", background="#2f0f07", text="Selecione o modelo que deseja alterar.")
        main_label.pack() 

        # Button to edit Consulta text model
        consulta = ttk.Button(self.root, text="Consulta", command=lambda: edit_message_model("Consulta"))
        consulta.pack()

        # Button to edit Cortesia text model
        cortesia = ttk.Button(self.root, text="Sessão de Cortesia", command=lambda: edit_message_model("Cortesia"))
        cortesia.pack()

        # Button to edit Plantão text model
        plantao = ttk.Button(self.root, text="Plantão", command=lambda: edit_message_model("Plantao"))
        plantao.pack()

        # Button to edit Missões text model
        missoes = ttk.Button(self.root, text="Missões", command=lambda: edit_message_model("Missoes"))
        missoes.pack()

        # Button to edit Dicas file or text model
        dicas = ttk.Button(self.root, text="Dicas", command=lambda: edit_file_or_message("Dicas"))
        dicas.pack()

        # Button to edit Feedback text model
        feedback = ttk.Button(self.root, text="Feedback", command=lambda: edit_message_model("Feedback"))
        feedback.pack()

        # Button to edit Contatos file or text model
        contatos = ttk.Button(self.root, text="Contatos", command=lambda: edit_file_or_message("Contatos"))
        contatos.pack()

        # Go back button
        goback = ttk.Button(self.root, text="Voltar", command=self.main_menu)
        goback.pack()

    # Function to set sending message window
    def messages(self, sheet):
        
        # Clear window
        self.clear_window()
        self.robot_logo()

        # Send messages label
        label = ttk.Label(self.root, text=f"Enviando mensagens \npara {sheet}...", font=('Arial', 32), background="#2f0f07", foreground="#ccc", padding="30 50 30 0")
        label.pack()
        
        # Function to get sending message results 
        def send_message():
            
            # Get result
            result = send_messages(sheet)

            # If result
            if result:

                # Result can be an int (200 or 500) if successful or failure
                if type(result) == int:
                    if result == 200:
                        message_box("info", "Resultados de Envio", f"Mensagens enviadas para {sheet} com sucesso.")
                
                # Or the messagebox itself
                else:
                    result()
            
            # Return to main menu
            self.clear_window()
            self.main_menu()

        # Run script after screen is loaded
        self.root.after(500, send_message)

        return

    # Clear window function
    def clear_window(self):
         
         # Destroy all widgets
        for item in self.root.winfo_children():
            item.destroy()

        return

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