from ..weather.Robust_Entry import RobustEntry

def validate_city(city):
    """
    Valida y corrige el nombre de la ciudad.
    Args:
        city (str): Nombre de la ciudad ingresada.
    Returns:
        tuple: Ciudad corregida o mensaje de error.
    """
    city_well_written = RobustEntry(city).get_city_well_written()

    if 'error' in city_well_written:
        return None, city_well_written['error']
    elif 'suggestion' in city_well_written:
        return None, city_well_written['message']

    return city_well_written['city'], None
