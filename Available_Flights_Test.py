import pytest
import pandas as pd
from app.services.Available_Flights import Flights

df = pd.read_csv('dataset1.csv')

@pytest.fixture
def flights_instance():
    return Flights()

def test_get_origin_coordinates_valid(flights_instance):
    """
    Prueba para obtener las coordenadas de una ciudad de origen válida.
    """
    origin_city = df['origin'].iloc[0]
    result = flights_instance.get_origin_coordinates(origin_city)
    assert 'origin_latitude' in result
    assert 'origin_longitude' in result


def test_get_origin_coordinates_invalid(flights_instance):
    """
    Prueba para obtener coordenadas de una ciudad de origen inválida.
    """
    result = flights_instance.get_origin_coordinates("InvalidCity")
    assert 'error' in result
    assert "No se encontraron coordenadas para la ciudad de origen" in result['error']


def test_get_destination_coordinates_valid(flights_instance):
    """
    Prueba para obtener las coordenadas de una ciudad de destino válida.
    """
    destination_city = df['destination'].iloc[0]  # Obtiene la primera ciudad de destino en el dataset
    result = flights_instance.get_destination_coordinates(destination_city)
    assert 'destination_latitude' in result
    assert 'destination_longitude' in result


def test_get_destination_coordinates_invalid(flights_instance):
    """
    Prueba para obtener coordenadas de una ciudad de destino inválida.
    """
    result = flights_instance.get_destination_coordinates("InvalidCity")
    assert 'error' in result
    assert "No se encontraron coordenadas para la ciudad de destino" in result['error']


def test_get_available_flights_by_destination_valid(flights_instance):
    """
    Prueba para obtener vuelos disponibles para un destino válido.
    """
    destination_city = df['destination'].iloc[0]
    result = flights_instance.get_available_flights_by_destination([destination_city])
    assert len(result) > 0


def test_get_available_flights_by_destination_invalid(flights_instance):
    """
    Prueba para obtener vuelos disponibles para un destino inválido.
    """
    result = flights_instance.get_available_flights_by_destination(["InvalidCity"])
    assert len(result) == 0


def test_get_available_flights_by_origin_valid(flights_instance):
    """
    Prueba para obtener vuelos disponibles para un origen válido.
    """
    origin_city = df['origin'].iloc[0]
    result = flights_instance.get_available_flights_by_origin([origin_city])
    assert len(result) > 0  


def test_get_available_flights_by_origin_invalid(flights_instance):
    """
    Prueba para obtener vuelos disponibles para un origen inválido.
    """
    result = flights_instance.get_available_flights_by_origin(["InvalidCity"])
    assert len(result) == 0 