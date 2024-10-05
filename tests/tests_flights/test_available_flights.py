import pytest
import pandas as pd
from app.services.flights.Available_Flights import Flights

df = pd.read_csv('dataset1.csv')

@pytest.fixture
def flights_instance():
    return Flights()

def test_get_available_flights_by_destination(flights_instance):
    """
    Test básico para el destino "PHX"
    """
    result = flights_instance.get_available_flights_by_destination(['PHX'])
    expected = [
        {'origin': 'HMO', 'destination': 'PHX', 'origin_latitude': 29.0959, 'origin_longitude': -111.048, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'MEX', 'destination': 'PHX', 'origin_latitude': 19.4363, 'origin_longitude': -99.0721, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
        {'origin': 'GDL', 'destination': 'PHX', 'origin_latitude': 20.5218, 'origin_longitude': -103.311, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
    ]
    assert result == expected

def test_get_available_flights_by_origin(flights_instance):
    """
    Test básico para el origen "HMO"
    """
    result = flights_instance.get_available_flights_by_origin(['HMO'])
    expected = [
        {'origin': 'HMO', 'destination': 'MEX', 'origin_latitude': 29.0959, 'origin_longitude': -111.048, 'destination_latitude': 19.4363, 'destination_longitude': -99.0721},
        {'origin': 'HMO', 'destination': 'PHX', 'origin_latitude': 29.0959, 'origin_longitude': -111.048, 'destination_latitude': 33.4343, 'destination_longitude': -112.012},
    ]
    assert result == expected

def test_get_available_flights_invalid_destination(flights_instance):
    """
    Test para un destino que no existe
    """
    result = flights_instance.get_available_flights_by_destination(['XYZ'])
    assert result == []

def test_get_available_flights_invalid_origin(flights_instance):
    """
    Test para un origen que no existe
    """
    result = flights_instance.get_available_flights_by_origin(['XYZ'])
    assert result == []