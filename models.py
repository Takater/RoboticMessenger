import json

# Models variable
models = {}

# Set models
with open('message_models.json', 'r') as file:
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

            # Return model with name, date and time
            return message_model.replace("{{nome}}", name).replace("{{data}}", date).replace("{{horario}}", hour)
        
        # If another column
        else:

            # Retrieve correct message model from models, according to type
            message_model = models['PACIENTES'][type] if (
                
                type not in ['DICAS', 'CONTATO']       #  If true, above result
                
                ) else models['PACIENTES'][type]['text']    #   Object's text

            # Return model with name
            return message_model.replace("{{nome}}", name)
    
    # Get models function
    def get_model(type = None):
        
        # Return all models or specific one
        return models if not type else models[type]
    
    # Edit models function
    def edit_model(model, **model_data):
        
        # Set models dictionary
        models = {}

        # Get new text 
        new_text = model_data.get("new_text")
        
        # Get models
        with open('message_models.json', "r") as file:
            models = json.load(file)
        
        
        if model not in ['DICAS', 'CONTATO']:
            # Overwrite chosen model
            models[model] = new_text
        
        else:
            new_file = model_data.get("new_file")
            
            if new_file:
                models[model]['file'] = new_file

            if new_text:
                models[model]['text'] = new_text


        # Overwrite models
        with open('message_models.json', 'w') as file:
            json.dump(models, file, indent = 2)


