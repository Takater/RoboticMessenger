# Messages Model
class Message:
    def __init__(self, type, **user_data):
        
        name = user_data.get("name")

        if (type == 'CONFIRMAR CONSULTA'):
            ""
