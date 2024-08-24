import requests
from time import time

# Diccionario para almacenar el caché
cache = {}

def get_weather_data(city, user_type):
    cache_key = (city, user_type)  
    
    # Verifica si la clave ya está en caché y no ha expirado
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time() - timestamp < 600:
            return cached_data

    # Si no está en caché o ha expirado, hacer una solicitud a la API
    api_key = 'cfb729fa224a70bb905e7e69682df89d'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
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
