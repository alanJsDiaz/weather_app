import pytest
from unittest.mock import patch
from app.services.helpers.api_helpers import fetch_weather_data

@patch('app.services.helpers.api_helpers.requests.get')
def test_fetch_weather_data_success(mock_get):
    """
    Prueba para respuesta exitosa (200 OK)
    """
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'weather': [{'description': 'clear sky'}],
        'main': {'temp': 25.0}
    }
    
    data, error = fetch_weather_data('fake_api_key', 'Mexico City')
    
    assert error is None
    assert data['weather'][0]['description'] == 'clear sky'
    assert data['main']['temp'] == 25.0

@patch('app.services.helpers.api_helpers.requests.get')
def test_fetch_weather_data_city_not_found(mock_get):
    """
    Prueba para ciudad no encontrada (404)
    """
    mock_response = mock_get.return_value
    mock_response.status_code = 404
    
    data, error = fetch_weather_data('fake_api_key', 'Unknown City')
    
    assert data is None
    assert error == "La ciudad 'Unknown City' no existe. Por favor, verifica el nombre e inténtalo de nuevo."

@patch('app.services.helpers.api_helpers.requests.get')
def test_fetch_weather_data_api_error(mock_get):
    """
    Prueba para otro error de la API (500 Internal Server Error)
    """
    mock_response = mock_get.return_value
    mock_response.status_code = 500
    
    data, error = fetch_weather_data('fake_api_key', 'Mexico City')
    
    assert data is None
    assert error == 'No se pudieron recuperar los datos del clima.'
