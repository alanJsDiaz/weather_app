from flask import Blueprint, render_template, request, redirect, url_for
from .services.weather_service import WeatherService
from .services.Robust_Entry import RobustEntry
import hashlib
import csv

main = Blueprint('main', __name__)

def load_passwords():
    """
    Lee las contraseñas desde el archivo passwords.txt y las devuelve en un diccionario.
    La primera línea es la contraseña de sobrecargo y la segunda la de piloto.
    """
    try:
        with open('passwords.txt', 'r') as file:
            lines = file.readlines()
            sobrecargo_password = lines[0].strip()
            piloto_password = lines[1].strip()
            return {
                'sobrecargo': sobrecargo_password,
                'piloto': piloto_password
            }
    except FileNotFoundError:
        print("Error: No se encontró el archivo passwords.txt")
        return None
    except IndexError:
        print("Error: El archivo passwords.txt no tiene el formato esperado.")
        return None

@main.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    suggestion_message = None

    USER_PASSWORDS = load_passwords()
    if not USER_PASSWORDS:
        error_message = "Error al cargar las contraseñas. Contacte al administrador."
        return render_template('index.html', error=error_message)

    if request.method == 'POST':
        city = request.form.get('city')
        user_type = request.form.get('user_type')
        password = request.form.get('password') 
        if not city or not user_type:
            error_message = "Por favor, ingresa una ciudad y selecciona un tipo de usuario."
            return render_template('index.html', error=error_message)

        if user_type in ['sobrecargo', 'piloto']:
            if not password:  
                error_message = f"Por favor, ingresa la contraseña para {user_type}."
                return render_template('index.html', error=error_message)
            elif password != USER_PASSWORDS.get(user_type): 
                error_message = "Contraseña incorrecta. Intenta de nuevo."
                return render_template('index.html', error=error_message)

        weather_service = WeatherService()
        weather_data = weather_service.get_weather_data(city, user_type)

        if isinstance(weather_data, dict) and 'error' in weather_data:
            error_message = weather_data['error']
            return render_template('index.html', error=error_message)

        return render_template('result.html', data=weather_data, user_type=user_type)

    return render_template('index.html', error=error_message)

@main.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')

        origin_entry = RobustEntry(origin).get_city_well_written()
        destination_entry = RobustEntry(destination).get_city_well_written()

        if 'error' in origin_entry:
            error_message = origin_entry['error']
            return render_template('ticket.html', error=error_message)
        elif 'suggestion' in origin_entry:
            suggestion_message = origin_entry['message']
            return render_template('ticket.html', suggestion=suggestion_message)

        if 'error' in destination_entry:
            error_message = destination_entry['error']
            return render_template('ticket.html', error=error_message)
        elif 'suggestion' in destination_entry:
            suggestion_message = destination_entry['message']
            return render_template('ticket.html', suggestion=suggestion_message)

        origin = origin_entry['city']
        destination = destination_entry['city']

        ticket = generate_ticket(origin, destination)

        save_ticket_to_csv(origin, destination, ticket)

        return render_template('ticket_result.html', ticket=ticket)

    return render_template('ticket.html')

def generate_ticket(origin, destination):
    """
    Genera un código alfanumérico a partir de la ciudad de origen y destino usando una función hash.
    """
    combined = origin + destination

    hash_object = hashlib.sha256(combined.encode())

    ticket_code = hash_object.hexdigest()[:6].upper()  
    return ticket_code

def save_ticket_to_csv(origin, destination, ticket):
    """
    Guarda el ticket generado junto con la ciudad de origen y destino en un archivo CSV.
    """
    with open('tickets.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([origin, destination, ticket])

@main.route('/consultar_por_ticket', methods=['GET', 'POST'])
def consultar_por_ticket():
    USER_PASSWORDS = load_passwords()
    if not USER_PASSWORDS:
        error_message = "Error al cargar las contraseñas. Contacte al administrador."
        return render_template('ticket_search.html', error=error_message)

    if request.method == 'POST':
        ticket = request.form.get('ticket')
        user_type = request.form.get('user_type')
        password = request.form.get('password')  
        if not ticket or not user_type:
            error_message = "Por favor, ingresa un ticket válido y selecciona un tipo de usuario."
            return render_template('ticket_search.html', error=error_message)

        if user_type in ['sobrecargo', 'piloto']:
            if not password:  
                error_message = f"Por favor, ingresa la contraseña para {user_type}."
                return render_template('ticket_search.html', error=error_message)
            elif password != USER_PASSWORDS.get(user_type): 
                error_message = "Contraseña incorrecta. Intenta de nuevo."
                return render_template('ticket_search.html', error=error_message)

        origin, destination = search_ticket_in_csv(ticket)

        if not destination:
            error_message = f"No se encontró el ticket: {ticket}."
            return render_template('ticket_search.html', error=error_message)

        weather_service = WeatherService()
        weather_data = weather_service.get_weather_data(destination, user_type)

        if isinstance(weather_data, dict) and 'error' in weather_data:
            error_message = weather_data['error']
            return render_template('ticket_search.html', error=error_message)

        return render_template('result.html', data=weather_data, user_type=user_type, origin=origin, destination=destination)

    return render_template('ticket_search.html')

def search_ticket_in_csv(ticket):
    """
    Busca un ticket en el archivo CSV y devuelve las ciudades de origen y destino asociadas.
    Args:
        ticket (str): El ticket que se desea buscar.
    Returns:
        tuple: Las ciudades de origen y destino si se encuentra, None si no se encuentra.
    """
    try:
        with open('tickets.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[2] == ticket:  
                    return row[0], row[1]  
    except FileNotFoundError:
        return None, None
    return None, None
