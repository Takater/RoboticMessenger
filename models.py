import json, shutil, os, codecs

# Models variable
models = {}

# Set models
with codecs.open('message_models.json', 'r', encoding="utf-8") as file:
    models = json.load(file)

# Messages Model 
class Message:

    # Get a message model
    def __init__(self, type, **user_data):
        
        # Person name
        name = user_data.get("name")

        # Message model variable
        message_model = ''

        # If column which includes date and time -> 'CONFIRMAR CONSULTA', 'CONFIRMAR CORTESIA'
        if 'CONFIRMAR' in type:
            
            # Get date and time
            date = user_data.get("date")
            hour = user_data.get("hour")
            
            # Get correct message model from models according to the second piece of type
            message_model = models["PACIENTES"][type.split()[1]]

            # Set message to model with name, date and time
            self.message = message_model.replace("{{nome}}", name).replace("{{data}}", date).replace("{{horario}}", hour)
            return
        
        # If another column
        else:

            # Retrieve correct message model from models, according to type
            if type not in ['DICAS', 'CONTATOS']:
                
                # Regular patient types
                message_model = models['PACIENTES'][type] 

            # If tips
            elif type == 'DICAS':

                # Set message
                message_model = models['PACIENTES'][type]['text'] 

                # Set image file
                self.image = models['PACIENTES'][type]['file']
            
            # If contact
            else:
                # Set message
                message_model = models[type]['text']

                # Set image file
                self.image = models[type]['file']

            # Set message to model with name
            self.message = message_model.replace("{{nome}}", name)

            # Finish initiating function
            return
    
# Get models function
def get_model(type = None):

    global models

    with codecs.open('message_models.json', 'r', encoding="utf-8") as file:
        models = json.load(file)
    
    # Return all models if no type
    if not type:
        return models
    
    # Specific type
    else:

        type = type.upper()

        # Retrieve correct type
        return models[type] if type == "CONTATOS" else models["PACIENTES"][type]
    
# Edit models function
def edit_model(model, **model_data):

    # Get new text 
    new_text = model_data.get("new_text")
    
    try:
        # Get models
        with codecs.open('message_models.json', "r", encoding="utf-8") as file:
            models = json.load(file)
        
        # If model is only text
        if model not in ['DICAS', 'CONTATOS']:

            # Overwrite chosen model
            models['PACIENTES'][model] = new_text
        
        # If model has both file and text
        else:

            # Get new file path
            new_file = model_data.get("new_file")
            
            # If there's a new file
            if new_file != None:

                # Get file name
                filename = os.path.basename(new_file)

                # Set destination folder to project's root
                destination = os.path.normpath(os.path.join(os.getcwd(), 'Files', filename)) if filename else ''

                # Copy file to destination if there's a file
                if filename:
                    shutil.copy(new_file, destination)

                # Set file path on models file according to selected model
                if model == 'CONTATOS':
                    
                    # Contatos model
                    models[model]['file'] = destination
                else:

                    # Dicas model
                    models['PACIENTES'][model]['file'] = destination

            # If there's a new text
            if new_text:

                # If Contatos model
                if model == 'CONTATOS':

                    # Overwrite model's text
                    models[model]['text'] = new_text
                
                # If Dicas model
                else:

                    # Overwrite model's text
                    models['PACIENTES'][model]['text'] = new_text

        # Overwrite models
        with codecs.open('message_models.json', 'w', encoding="utf-8") as file:
            json.dump(models, file, indent = 2, ensure_ascii=False)

        return 200
    
    except:
        return 500


