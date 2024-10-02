from ..weather.weather_service import WeatherService

def get_weather_data_for_user(city, user_type):
    """
    Función auxiliar para obtener datos de clima para un usuario específico.
    """
    weather_service = WeatherService()
    weather_data = weather_service.get_weather_data(city, user_type)

    if isinstance(weather_data, dict) and 'error' in weather_data:
        return None, weather_data['error']

    return weather_data, None