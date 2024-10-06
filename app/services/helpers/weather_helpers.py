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

def get_recommendations(temperature):
    if temperature <= 0:
        return ["Lleva ropa térmica para mantener el calor.", "Evita estar afuera por mucho tiempo."]
    elif 0 < temperature <= 10:
        return ["Usa una chaqueta o abrigo ligero.", "Es recomendable beber bebidas calientes."]
    elif 10 < temperature <= 20:
        return ["Usa ropa ligera pero con una capa adicional.", "Considera una bufanda por si la temperatura baja más tarde."]
    elif 20 < temperature <= 30:
        return ["Usa ropa fresca y ligera.", "Mantente hidratado durante el día."]
    else:
        return ["Usa protector solar y mantente a la sombra.", "Evita la actividad física intensa bajo el sol."]