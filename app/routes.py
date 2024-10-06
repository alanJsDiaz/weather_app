from flask import Blueprint, render_template, request
from .services.weather.weather_service import WeatherService
from .services.weather.Robust_Entry import RobustEntry
from .services.helpers.form_helpers import get_form_data, validate_form_data, get_ticket_form_data, get_origin_destination
from .services.helpers.ticket_helpers import generate_ticket, save_ticket_to_csv, search_ticket_in_csv, process_ticket_entries
from .services.helpers.template_helpers import render_template_with_error
from .services.helpers.weather_helpers import get_weather_data_for_user
from .services.helpers.weather_helpers import get_recommendations

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

    USER_PASSWORDS = load_passwords()
    if not USER_PASSWORDS:
        return render_template_with_error('index.html', "Error al cargar las contraseñas. Contacte al administrador.")

    if request.method == 'POST':
        city, user_type, password = get_form_data()

        error_message = validate_form_data(city, user_type, password, USER_PASSWORDS)
        if error_message:
            return render_template_with_error('index.html', error_message)

        weather_data, error_message = get_weather_data_for_user(city, user_type)
        if error_message:
            return render_template_with_error('index.html', error_message)
        
        recomendaciones = get_recommendations(weather_data['temperature'])

        return render_template('result.html', data=weather_data, user_type=user_type, recommendations=recomendaciones)

    return render_template('index.html', error=error_message)


@main.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        origin, destination = get_origin_destination()

        origin_entry, destination_entry, suggestion_message, error_message = process_ticket_entries(origin, destination)

        if error_message:
            return render_template_with_error('ticket.html', error_message)
        if suggestion_message:
            return render_template('ticket.html', suggestion=suggestion_message)

        ticket = generate_ticket(origin_entry['city'], destination_entry['city'])
        save_ticket_to_csv(origin_entry['city'], destination_entry['city'], ticket)

        return render_template('ticket_result.html', ticket=ticket)

    return render_template('ticket.html')

@main.route('/consultar_por_ticket', methods=['GET', 'POST'])
def consultar_por_ticket():
    USER_PASSWORDS = load_passwords()
    if not USER_PASSWORDS:
        return render_template_with_error('ticket_search.html', "Error al cargar las contraseñas. Contacte al administrador.")

    if request.method == 'POST':
        ticket, user_type, password = get_ticket_form_data()
        
        error_message = validate_form_data(ticket, user_type, password, USER_PASSWORDS)
        if error_message:
            return render_template_with_error('ticket_search.html', error_message)

        origin, destination = search_ticket_in_csv(ticket)
        if not destination:
            return render_template_with_error('ticket_search.html', f"No se encontró el ticket: {ticket}.")

        weather_data, error_message = get_weather_data_for_user(destination, user_type)
        if error_message:
            return render_template_with_error('ticket_search.html', error_message)
        
        recomendaciones = get_recommendations(weather_data['temperature'])

        return render_template('result.html', data=weather_data, user_type=user_type, origin=origin, destination=destination,recommendations=recomendaciones)

    return render_template('ticket_search.html')



