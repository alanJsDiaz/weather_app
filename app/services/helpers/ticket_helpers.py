import hashlib
import csv
from ..weather.Robust_Entry import RobustEntry

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

def search_ticket_in_csv(ticket):
    """
    Busca un ticket en el archivo CSV y devuelve las ciudades de origen y destino asociadas.
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

def process_ticket_entries(origin, destination):
    """
    Procesa y valida las entradas de las ciudades de origen y destino.
    """
    origin_entry = RobustEntry(origin).get_city_well_written()
    destination_entry = RobustEntry(destination).get_city_well_written()

    suggestion_message = None
    error_message = None

    if 'error' in origin_entry:
        error_message = origin_entry['error']
    elif 'suggestion' in origin_entry:
        suggestion_message = origin_entry['message']

    if 'error' in destination_entry:
        error_message = destination_entry['error']
    elif 'suggestion' in destination_entry:
        suggestion_message = destination_entry['message']

    return origin_entry, destination_entry, suggestion_message, error_message
