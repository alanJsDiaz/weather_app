import pytest
from unittest.mock import patch, mock_open
from app.services.weather.weather_service import WeatherService

@patch('builtins.open', new_callable=mock_open, read_data='fake_api_key')
def test_weather_service_initialization(mock_file):
    """
    Prueba para la inicialización del servicio y carga de API key correctamente
    """
    service = WeatherService()
    assert service.api_key == 'fake_api_key'

@patch('builtins.open', side_effect=FileNotFoundError)
def test_weather_service_api_key_file_not_found(mock_file):
    """
    Prueba para manejo de excepción si el archivo api_key.txt no existe
    """
    with pytest.raises(Exception) as excinfo:
        WeatherService()
    assert "El archivo 'api_key.txt' no fue encontrado" in str(excinfo.value)

@patch('builtins.open', side_effect=Exception("Otro error"))
def test_weather_service_api_key_generic_exception(mock_file):
    """
    Prueba para cuando ocurre otro tipo de excepción
    """
    with pytest.raises(Exception) as excinfo:
        WeatherService()
    assert "Otro error" in str(excinfo.value)

@patch('app.services.weather.weather_service.WeatherService.load_api_key', return_value='fake_api_key')
@patch('app.services.weather.weather_service.validate_city', return_value=('Mexico City', None))
@patch('app.services.weather.weather_service.is_cached', return_value=False)
@patch('app.services.weather.weather_service.fetch_weather_data', return_value=({'temperature': 25.0, 'description': 'clear sky'}, None))
@patch('app.services.weather.weather_service.WeatherService.create_weather_data', return_value={'city': 'Mexico City', 'temperature': 25.0, 'description': 'clear sky'})    
@patch('app.services.weather.weather_service.store_in_cache')
def test_get_weather_data(mock_store_in_cache, mock_create_weather_data, mock_fetch_weather_data, mock_is_cached, mock_validate_city, mock_load_api_key):
    """
    Prueba para obtener datos del clima correctamente y almacenarlos en caché 
    """
    service = WeatherService()
    data = service.get_weather_data('Mexico City', 'turista')
    assert data == {'city': 'Mexico City', 'temperature': 25.0, 'description': 'clear sky'}
    mock_store_in_cache.assert_called_once()
    mock_create_weather_data.assert_called_once()


@patch('app.services.weather.weather_service.WeatherService.load_api_key', returnvalue='fake_api_key')
@patch('app.services.weather.weather_service.validate_city', return_value=(None, 'City not found'))
def test_get_weather_data_invalid_city(mock_validate_city, mock_load_api_key):
    """
    Prueba para obtener datos del clima con error al validar la ciudad
    """
    service = WeatherService()
    data = service.get_weather_data('Invalid City', 'turista')
    assert data == {'error': 'City not found'}
    mock_validate_city.assert_called_once()
    mock_load_api_key.assert_called_once()
