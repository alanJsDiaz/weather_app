
import pytest
from unittest.mock import patch
from app.services.helpers.city_helpers import validate_city

@patch('app.services.weather.Robust_Entry.RobustEntry.get_city_well_written', return_value={'city': 'Mexico City'})
def test_validate_city_success(mock_get_city_well_written):
    """
    Prueba para validar una ciudad correctamente
    """
    city, error = validate_city('Mexico City')
    assert city == 'Mexico City'
    assert error is None

@patch('app.services.weather.Robust_Entry.RobustEntry.get_city_well_written', return_value={'error': 'Ciudad no encontrada'})
def test_validate_city_error(mock_get_city_well_written):
    """
    Prueba para una ciudad con errores
    """
    city, error = validate_city('Invalid City')
    assert city is None
    assert error == 'Ciudad no encontrada'

@patch('app.services.weather.Robust_Entry.RobustEntry.get_city_well_written', return_value={'suggestion': True, 'message': 'Did you mean: Mexico City?'})
def test_validate_city_suggestion(mock_get_city_well_written):
    """
    Prueba para una ciudad con sugerencias
    """
    city, error = validate_city('Mexio City')
    assert city is None
    assert error == 'Did you mean: Mexico City?'
