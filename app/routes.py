from flask import Blueprint, render_template, request,redirect,url_for
from .services.weather_service import WeatherService
from .services.Robust_Entry import RobustEntry
import hashlib
import csv


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    suggestion_message = None

    if request.method == 'POST':
        city = request.form.get('city')
        user_type = request.form.get('user_type')

        # Validación de campos del formulario
        if not city or not user_type:
            error_message = "Por favor, ingresa una ciudad y selecciona un tipo de usuario."
            return render_template('index.html', error=error_message)

        weather_service = WeatherService()
        weather_data = weather_service.get_weather_data(city, user_type)

        if isinstance(weather_data, dict) and 'error' in weather_data:
            error_message = weather_data['error']
            return render_template('index.html', error=error_message)

        return render_template('result.html', data=weather_data, user_type=user_type)

    # Renderizar la página principal en caso de GET o de error
    return render_template('index.html', error=error_message)

@main.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')

        # Validación de las ciudades de origen y destino
        origin_entry = RobustEntry(origin).get_city_well_written()
        destination_entry = RobustEntry(destination).get_city_well_written()

        # Verifica si hay un error en la ciudad de origen o destino
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

        # Si las ciudades son válidas, se genera el ticket usando la ciudad corregida o bien escrita
        origin = origin_entry['city']
        destination = destination_entry['city']

        # Generar el ticket usando la función hash
        ticket = generate_ticket(origin, destination)

        # Guardar la información en un archivo CSV
        save_ticket_to_csv(origin, destination, ticket)

        # Mostrar el ticket generado al usuario
        return render_template('ticket_result.html', ticket=ticket)

    return render_template('ticket.html')


def generate_ticket(origin, destination):
    """
    Genera un código alfanumérico a partir de la ciudad de origen y destino usando una función hash.
    """
    # Crear una cadena combinando la ciudad de origen y destino
    combined = origin + destination

    # Crear un hash a partir de la cadena combinada
    hash_object = hashlib.sha256(combined.encode())

    # Convertir el hash en una cadena alfanumérica y devolver los primeros 6 caracteres
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
    if request.method == 'POST':
        ticket = request.form.get('ticket')
        user_type = request.form.get('user_type')

        # Verificar que se ingrese un ticket y tipo de usuario
        if not ticket or not user_type:
            error_message = "Por favor, ingresa un ticket válido y selecciona un tipo de usuario."
            return render_template('ticket_search.html', error=error_message)

        # Buscar el ticket en el CSV
        destination = search_ticket_in_csv(ticket)

        if destination is None:
            error_message = f"No se encontró el ticket: {ticket}."
            return render_template('ticket_search.html', error=error_message)

        # Si se encontró el destino, hacemos la consulta del clima
        weather_service = WeatherService()
        weather_data = weather_service.get_weather_data(destination, user_type)

        if isinstance(weather_data, dict) and 'error' in weather_data:
            error_message = weather_data['error']
            return render_template('ticket_search.html', error=error_message)

        return render_template('result.html', data=weather_data, user_type=user_type)

    return render_template('ticket_search.html')

def search_ticket_in_csv(ticket):
    """
    Busca un ticket en el archivo CSV y devuelve la ciudad de destino asociada.
    Args:
        ticket (str): El ticket que se desea buscar.
    Returns:
        str: La ciudad de destino si se encuentra, None si no se encuentra.
    """
    try:
        with open('tickets.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[2] == ticket:  # Verificamos la columna "ticket"
                    return row[1]  # Retornamos la ciudad destino
    except FileNotFoundError:
        return None
    return None
