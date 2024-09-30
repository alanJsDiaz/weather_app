import requests
from time import time
from app.services.Robust_Entry import RobustEntry
from app.services.Available_Flights import Flights

class WeatherService:
    def __init__(self):
        """
        Inicializa el objeto WeatherService.
        """
        self.cache = {}



    def get_weather_data(self, city, user_type):
        """
        Recupera los datos climáticos para una ciudad y tipo de usuario dados.
        Args:
            city (str): El nombre de la ciudad.
            user_type (str): El tipo de usuario.
        Returns:
            dict: Un diccionario que contiene los datos climáticos para la ciudad.         """
        city_well_written = RobustEntry(city).get_city_well_written()
        if city_well_written == 'error':
            return {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}
        iata = RobustEntry(city_well_written).get_iata()
        cache_key = (city_well_written, user_type)
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time() - timestamp < 600:
                return cached_data
        api_key = 'cfb729fa224a70bb905e7e69682df89d'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_well_written}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 404:
            return {'error': f"La ciudad '{city_well_written}' no existe. Por favor, verifica el nombre e inténtalo de nuevo."}
        elif response.status_code != 200:
            return {'error': 'No se pudieron recuperar los datos'}
        avalaible_flights = Flights().get_available_flights_by_origin(iata)
        data = response.json()
        result = self.create_weather_data(data, avalaible_flights, user_type)
        self.cache[cache_key] = (result, time())
        return result
    
    
    
    def create_weather_data(self, data, avalaible_flights, user_type):
        '''Crea datos meteorológicos basados en el tipo de usuario.
        Args:
        - data: Los datos meteorológicos.
        - avalaible_flights: Los vuelos disponibles.
        - user_type: El tipo de usuario.
        Return:
        - Si el tipo de usuario es 'turista', retorna una instancia de TuristaWeatherData.
        - Si el tipo de usuario es 'sobrecargo', retorna una instancia de SobrecargoWeatherData.
        - Si el tipo de usuario es 'piloto', retorna una instancia de PilotoWeatherData.
        - Si el tipo de usuario es inválido, retorna un diccionario con un mensaje de error.
        '''
        if user_type == 'turista':
            return TuristaWeatherData(data, avalaible_flights)
        elif user_type == 'sobrecargo':
            return SobrecargoWeatherData(data, avalaible_flights)
        elif user_type == 'piloto':
            return PilotoWeatherData(data, avalaible_flights)
        else:
            return {'error': 'Tipo de usuario invalido.'}


class WeatherData:
    def __init__(self, data, avalaible_flights):
        self.city = data['name']
        self.temperature = data['main']['temp']
        self.flights = avalaible_flights  


class TuristaWeatherData(WeatherData):
    def __init__(self, data, avalaible_flights):
        super().__init__(data, avalaible_flights)
        self.description = data['weather'][0]['description']


class SobrecargoWeatherData(WeatherData):
    def __init__(self, data, avalaible_flights):
        super().__init__(data, avalaible_flights)
        self.humidity = data['main']['humidity']


class PilotoWeatherData(WeatherData):
    def __init__(self, data, avalaible_flights):
        super().__init__(data, avalaible_flights)
        self.lat = data['coord']['lat']
        self.lon = data['coord']['lon']
        self.wind_speed = data['wind']['speed']
        self.wind_deg = data['wind']['deg']
        self.pressure = data['main']['pressure']