
import pytest
from unittest.mock import patch
from app.services.helpers.weather_helpers import get_weather_data_for_user

@patch('app.services.weather.weather_service.WeatherService.get_weather_data')
def test_get_weather_data_for_user_valid(mock_get_weather_data):
    """
    Prueba para get_weather_data_for_user: verificar que devuelve datos del clima válidos
    """
    mock_get_weather_data.return_value = {
        'city': 'Mexico City',
        'temperature': 25.0,
        'description': 'clear sky'
    }
    
    data, error = get_weather_data_for_user('Mexico City', 'turista')
    
    assert data == {
        'city': 'Mexico City',
        'temperature': 25.0,
        'description': 'clear sky'
    }
    assert error is None

@patch('app.services.weather.weather_service.WeatherService.get_weather_data')
def test_get_weather_data_for_user_error(mock_get_weather_data):
    """
    Prueba para get_weather_data_for_user: verificar que devuelve un error si hay un problema con los datos del clima
    """
    mock_get_weather_data.return_value = {
        'error': 'City not found'
    }
    
    data, error = get_weather_data_for_user('Unknown City', 'turista')
    
    assert data is None
    assert error == 'City not found'


