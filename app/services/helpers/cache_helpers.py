from time import time

def is_cached(cache, cache_key):
    """
    Verifica si los datos del clima están en caché y son válidos.
    Args:
        cache (dict): La caché.
        cache_key (tuple): Clave de la caché.
    Returns:
        bool: True si los datos están en caché y son válidos, False en caso contrario.
    """
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if time() - timestamp < 600:  # 10 minutos de caché
            return True
    return False

def store_in_cache(cache, cache_key, data):
    """
    Almacena los datos del clima en la caché.
    Args:
        cache (dict): La caché.
        cache_key (tuple): Clave de la caché.
        data (dict): Datos a almacenar.
    """
    cache[cache_key] = (data, time())
