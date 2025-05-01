from telegram import ReplyKeyboardMarkup


def build_role_menu(role: str):
    """
    Devuelve un ReplyKeyboardMarkup con las opciones que le corresponden
    al rol indicado: 'admin', 'professor' o 'student'.
    """

    # Define las opciones por rol
    options = {
        "admin": [
            ["Promover a profesor"], 
            ["Añadir curso", "Añadir tag a curso"]
        ],
        "professor": [
            ["Añadir curso", "Añadir tag a curso"]
        ],
        "student": [
            ["Seleccionar tags"], 
            ["Lista de optativas"]
        ]
    }

    # Obtén la lista de filas o una lista vacía si no existe el rol
    buttons = options.get(role, [])
    
    # Crea el ReplyKeyboardMarkup (botones permanentes bajo la caja de texto)  
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,    # ajusta la altura de los botones
        one_time_keyboard=False  # permanece hasta que se cambie
    )
