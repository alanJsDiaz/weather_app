import pytest
from app.services.weather.Robust_Entry import RobustEntry

def test_empty_city():
    """
    Prueba que la función maneje correctamente una entrada vacía para la ciudad.
    """
    entry = RobustEntry("")
    assert entry.get_city_well_written() == {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}

def test_none_city():
    """
    Prueba que la función maneje correctamente un valor None para la ciudad.
    """
    with pytest.raises(AttributeError):
        entry = RobustEntry(None)
        entry.get_city_well_written()

def test_case_insensitive():
    """
    Prueba que la función sea insensible a mayúsculas y minúsculas.
    """
    entry = RobustEntry("CAncUn")
    assert entry.get_city_well_written() == {'city': 'Cancun'}
    assert entry.get_iata() == ["CUN"]

def test_special_characters():
    """
    Prueba que la función maneje correctamente caracteres especiales en el nombre de la ciudad.
    """
    entry = RobustEntry("C@nCun!123")
    assert entry.get_city_well_written() == {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}

def test_city_similar_name():
    """
    Prueba el manejo de nombres de ciudades con errores menores, como omisiones de letras.
    """
    entry = RobustEntry("Cancu")  # Faltando una 'n'
    assert entry.get_city_well_written() == {'suggestion': 'Cancun', 'message': "La ciudad 'CANCU' no fue encontrada, ¿quisiste decir 'Cancun'?"}
    assert entry.get_iata() == []

def test_extremely_long_name():
    """
    Prueba que la función maneje nombres de ciudades extremadamente largos que no existen.
    """
    entry = RobustEntry("CiudadExtraordinariamenteLargaQueNoExiste")
    assert entry.get_city_well_written() == {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}

def test_city_not_in_list():
    """
    Prueba que la función maneje nombres de ciudades que no están en la lista y sugiera nombres similares.
    """
    entry = RobustEntry("Atlantis")
    assert entry.get_city_well_written() == {'suggestion': 'Atlanta', 'message': "La ciudad 'ATLANTIS' no fue encontrada, ¿quisiste decir 'Atlanta'?"}
    assert entry.get_iata() == []

def test_valid_iata():
    """
    Prueba que la función maneje correctamente un código IATA válido.
    """
    entry = RobustEntry('DFW')
    assert entry.get_city_well_written() == {'city': 'Dallas'}
    assert entry.get_iata() == ['DFW']

def test_invalid_city():
    """
    Prueba que la función maneje correctamente un nombre de ciudad no válido.
    """
    entry = RobustEntry('Cida')
    assert entry.get_city_well_written() == {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}
    assert entry.get_iata() == []

def test_valid_iata_2():
    """
    Prueba que la función maneje correctamente un código IATA válido en minúsculas.
    """
    entry = RobustEntry('yVr')
    assert entry.get_city_well_written() == {'city': 'Vancouver'}
    assert entry.get_iata() == ['YVR']

def test_valid_iata_3():
    """
    Prueba que la función devuelva correctamente el código IATA para 'yVr'.
    """
    entry = RobustEntry('yVr')
    assert entry.get_iata() == ['YVR']

def test_valid_iata_4():
    """
    Prueba que la función maneje correctamente el código IATA 'MEX' para Ciudad de México.
    """
    entry = RobustEntry('MEX')
    assert entry.get_city_well_written() == {'city': 'Ciudad de Mexico'}
    assert entry.get_iata() == ['MEX']

def test_invalid_iata():
    """
    Prueba que la función maneje correctamente un código IATA no válido.
    """
    entry = RobustEntry("XXX")
    assert entry.get_city_well_written() == {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}
    assert entry.get_iata() == []

def test_invalid_iata_2():
    """
    Prueba que la función sugiera una ciudad válida
    """
    entry = RobustEntry("CDMX")
    assert entry.get_city_well_written() == {'city': 'Ciudad de Mexico'}
    assert entry.get_iata() == ["MEX"]
