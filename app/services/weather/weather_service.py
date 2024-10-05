from ..helpers.api_helpers import fetch_weather_data
from ..helpers.cache_helpers import is_cached, store_in_cache
from ..helpers.city_helpers import validate_city
from ..helpers.data_formatter import TuristaWeatherData, SobrecargoWeatherData, PilotoWeatherData


class WeatherService:

    def __init__(self):
        """
        Inicializa el objeto WeatherService.
        """
        self.cache = {}
        self.api_key = self.load_api_key()


    def load_api_key(self):
        """
        Lee la clave API desde un archivo txt llamado 'api_key.txt'.
        Returns:
            str: La clave API si se lee correctamente, o None si ocurre algún error.
        """
        try:
            with open('api_key.txt', 'r') as file:
                api_key = file.read().strip()
                return api_key
        except FileNotFoundError:
            raise Exception("El archivo 'api_key.txt' no fue encontrado. Asegúrate de que existe y contiene la clave API.")
        except Exception as e:
            raise Exception(f"Error al leer la clave API: {str(e)}")


    def get_weather_data(self, city, user_type):
        """
        Recupera los datos climáticos para una ciudad y tipo de usuario dados.
        Args:
            city (str): El nombre de la ciudad.
            user_type (str): El tipo de usuario.
        Returns:
            dict: Un diccionario que contiene los datos climáticos para la ciudad.
        """
        city_well_written, error = validate_city(city)
        if error:
            return {'error': error}

        cache_key = (city_well_written, user_type)
        if is_cached(self.cache, cache_key):
            return self.cache[cache_key][0]

        weather_data, error = fetch_weather_data(self.api_key, city_well_written)
        if error:
            return {'error': error}

        result = self.create_weather_data(weather_data, user_type)
        store_in_cache(self.cache, cache_key, result)

        return result



    def create_weather_data(self, data, user_type):
        """
        Crea datos meteorológicos basados en el tipo de usuario.
        Args:
            data (dict): Los datos meteorológicos.
            user_type (str): El tipo de usuario.
        Returns:
            dict: Los datos formateados para el tipo de usuario.
        """
        if user_type == 'turista':
            return TuristaWeatherData(data).to_dict()
        elif user_type == 'sobrecargo':
            return SobrecargoWeatherData(data).to_dict()
        elif user_type == 'piloto':
            return PilotoWeatherData(data).to_dict()
        else:
            return {'error': 'Tipo de usuario inválido.'}