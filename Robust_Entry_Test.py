import pytest
from app.services.Robust_Entry import RobustEntry

def test_empty_city():
    entry = RobustEntry("")
    assert entry.get_city_well_written() == 'error'

def test_none_city():
    with pytest.raises(AttributeError):
        entry = RobustEntry(None)
        entry.get_city_well_written()

def test_case_insensitive():
    entry = RobustEntry("cAncUn")
    assert entry.get_city_well_written() == "Cancun"

def test_special_characters():
    entry = RobustEntry("C@nCun!123")
    assert entry.get_city_well_written() == 'error'

def test_city_similar_name():
    entry = RobustEntry("Cancu")  # Faltando una 'n'
    assert entry.get_city_well_written() == "Cancun"
    assert entry.get_iata() == ["CUN"]

def test_extremely_long_name():
    entry = RobustEntry("CiudadExtraordinariamenteLargaQueNoExiste")
    assert entry.get_city_well_written() == 'error'

def test_city_not_in_list():
    entry = RobustEntry("Atlantis")
    assert entry.get_city_well_written() == 'Atlanta'

def test_valid_iata():
    entry = RobustEntry('DFW')
    assert entry.get_city_well_written() == "Dallas"
    assert entry.get_iata() == ['DFW']

def test_invalid_city():
    entry = RobustEntry('Cida')
    assert entry.get_city_well_written() == "error"
    assert entry.get_iata() == []

def test_valid_iata_2():
    entry = RobustEntry('yVr')
    assert entry.get_city_well_written() == "Vancouver"
    assert entry.get_iata() == ['YVR']

def test_invalid_iata():
    entry = RobustEntry("XXX")
    assert entry.get_city_well_written() == "error"
    assert entry.get_iata() == []

def test_invalid_iata_2():
    entry = RobustEntry("CDMX")
    assert entry.get_city_well_written() == "Ciudad de Mexico"
    assert entry.get_iata() == ["MEX"]


