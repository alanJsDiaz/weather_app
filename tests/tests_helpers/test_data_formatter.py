
from app.services.helpers.data_formatter import WeatherData, TuristaWeatherData, SobrecargoWeatherData

def test_weather_data_formatting():
    """
    Prueba para WeatherData: verificar que se formatean correctamente la ciudad y la temperatura
    """
    data = {
        'name': 'Mexico City',
        'main': {'temp': 25.0}
    }
    weather_data = WeatherData(data)
    result = weather_data.to_dict()
    
    assert result['city'] == 'Mexico City'
    assert result['temperature'] == 25.0

def test_turista_weather_data_formatting():
    """
    Prueba para TuristaWeatherData: verificar que se añade la descripción del clima
    """
    data = {
        'name': 'Mexico City',
        'main': {'temp': 25.0},
        'weather': [{'description': 'clear sky'}]
    }
    turista_data = TuristaWeatherData(data)
    result = turista_data.to_dict()
    
    assert result['city'] == 'Mexico City'
    assert result['temperature'] == 25.0
    assert result['description'] == 'clear sky'

def test_sobrecargo_weather_data_formatting():
    """
    Prueba para SobrecargoWeatherData: verificar que se formatean los datos correctamente
    """
    data = {
        'name': 'Mexico City',
        'main': {'temp': 25.0, 'humidity': 80, 'visibility': 10000},
    }
    sobrecargo_data = SobrecargoWeatherData(data)
    result = sobrecargo_data.to_dict()
    
    assert result['city'] == 'Mexico City'
    assert result['temperature'] == 25.0
    assert result['humidity'] == 80
    assert result['visibility'] == 'N/A'
