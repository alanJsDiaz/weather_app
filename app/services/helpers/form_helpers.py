from flask import request

def get_form_data():
    """
    Extrae los datos del formulario para la ciudad, tipo de usuario y contraseña.
    """
    city = request.form.get('city')
    user_type = request.form.get('user_type')
    password = request.form.get('password')
    return city, user_type, password

def validate_form_data(city, user_type, password, USER_PASSWORDS):
    """
    Valida los datos del formulario: ciudad, tipo de usuario y contraseña.
    """
    if not city or not user_type:
        return "Por favor, ingresa una ciudad y selecciona un tipo de usuario."
    
    if user_type in ['sobrecargo', 'piloto']:
        if not password:
            return f"Por favor, ingresa la contraseña para {user_type}."
        elif password != USER_PASSWORDS.get(user_type):
            return "Contraseña incorrecta. Intenta de nuevo."
    
    return None

def get_ticket_form_data():
    """
    Extrae los datos del formulario de búsqueda de tickets.
    """
    ticket = request.form.get('ticket')
    user_type = request.form.get('user_type')
    password = request.form.get('password')
    return ticket, user_type, password

def get_origin_destination():
    """
    Extrae las ciudades de origen y destino del formulario de tickets.
    """
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    return origin, destination
