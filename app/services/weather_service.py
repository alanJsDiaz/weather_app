import requests
from time import time
from fuzzywuzzy import process


# Diccionario para almacenar el caché
cache = {}

def get_weather_data(city, user_type):

    # Lista de ciudades disponibles de acuaerdo al Csv proporcionado
    cities_available = ["Ciudad De Mexico","Toluca", "Cancun","Aguascalientes", "Guanajuato", "Chihuahua", "Cozumel", "Guadalajara", "Monterrey", "Puebla", "Puerto Vallarta", "Queretaro", "San Luis Potosi", "Torreon", "Acapulco", "Ciudad Juarez", "Ciudad del Carmen", "Chetumal", 
                        "Hermosillo", "Huatulco", "Merida", "Oaxaca","Puerto Escondido", "Tampico", "Tijuana", "Veracruz", "Zacatecas", "Ixtapa", "Zihuatanejo", "Villahermosa", "Amsterdam", "Atlanta", "Bogota", "Belice" , "Paris", "Ciudad Obregon",
                        "Charlotte", "Dalas", "Fort Worth", "Ciudad de Guatemala", "Havana", "Houston", "New York", "Los Angeles", "Lima", "Madrid", "Miami", "Mazatlan", "Philadelphia", "Phoenix", "Santiago", "Vancouver", "Toronto"]
    

    # IATA's de las ciudades disponibles
    iatas_cities_available = {
        "CDMX": "Ciudad De Mexico", "MTY" : "Monterrey", "QRO": "Queretaro", "CJS": "Ciudad Juarez", "HMO" : "Hermosillo", "CME":"Ciudad de Carmen", "HUX" : "Huatulco", "PVR": "Puerto Vallarta",
        "PXM" : "Puerto Escondido", "VSA" : "Villahermosa","CUU" : "Chihuahua", "TRC" : "Torreon", "BJX":"Leon", "PBC" : "Puebla", "ZCL" : "Zacatecas", "LAX" : "Los Angeles", "JFK": "Nueva York",
        "MZT" : "Mazatlan", "GUA" : "Ciudad de Guatemala", "DFW" : "Dallas", "ORD": "Chicago", "PHX" : "Phoenix", "PHL" : "Philadelphia", "CLT" : "Charlotte", "YYZ" : "Toronto", "IAH": "Houston", 
        "YVR" : "Vancouver", "CDG" : "Paris", "CEN" : "Ciudad Obregon", "SCL" : "Santiago", "SLP" : "San Luis Potosi"}

    # Procesamos la IATA ingresada por el usuario, asignandole la ciudad de la IATA, si no se ingresa una IATA e asigna la ciudad original ingresada por el usuario, tambien le quitamos los espacios preceden y proceden de la ciudad
    city = city.strip()
    city = iatas_cities_available.get(city, city)

    # Procesamos la ciudad ingresada por el usuario, asignandole la ciudad más parecida de la lista de ciudades disponibles
    city_well_written = process.extractOne(city, cities_available)

    # Si la similitud de la ciudad ingresada por el usuario con la ciudad más parecida de la lista de ciudades disponibles es menor a 64, se asigna el nombre original para que arroge que no existe esa ciudad
    if city_well_written[1] < 64:   
        city_well_written = city


    cache_key = (city_well_written[0], user_type)  
    
    # Verifica si la clave ya está en caché y no ha expirado
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time() - timestamp < 600:
            return cached_data

    # Si no está en caché o ha expirado, hacer una solicitud a la API
    api_key = 'cfb729fa224a70bb905e7e69682df89d'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_well_written[0]}&appid={api_key}&units=metric'
    response = requests.get(url)
    
    # Manejo de errores de respuesta de la API
    if response.status_code == 404:
        return {'error': f"La ciudad '{city}' no existe. Por favor, verifica el nombre e inténtalo de nuevo."}
    elif response.status_code != 200:
        return {'error': 'No se pudieron recuperar los datos'}

    data = response.json()

    # Procesar los datos según el tipo de usuario
    if user_type == 'turista':
        result = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
        }
    elif user_type == 'sobrecargo':
        result = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'visibility': data.get('visibility', 'N/A'),
        }
    elif user_type == 'piloto':
        result = {
            'city': data['name'],
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'pressure': data['main']['pressure'],
        }
    else:
        return {'error': 'Tipo de usuario invalido.'}
    
    # Almacenar los datos en caché junto con un timestamp
    cache[cache_key] = (result, time())

    return result
