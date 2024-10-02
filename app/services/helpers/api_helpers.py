import requests

def fetch_weather_data(api_key, city):
    """
    Realiza la solicitud a la API para obtener los datos del clima.
    Args:
        api_key (str): La clave de la API.
        city (str): El nombre de la ciudad bien escrita.
    Returns:
        tuple: Los datos de la API o un mensaje de error.
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 404:
        return None, f"La ciudad '{city}' no existe. Por favor, verifica el nombre e inténtalo de nuevo."
    elif response.status_code != 200:
        return None, 'No se pudieron recuperar los datos del clima.'

    return response.json(), None
