import pytest
from time import time
from app.services.helpers.cache_helpers import is_cached, store_in_cache

def test_is_cached_valid_data():
    """
    Prueba para is_cached: verifica que devuelve True si los datos están en caché y no han expirado
    """
    cache = {}
    cache_key = ('Mexico City', 'turista')
    data = {"weather": "sunny"}
    timestamp = time() - 300 
    cache[cache_key] = (data, timestamp)
    
    assert is_cached(cache, cache_key) == True

def test_is_cached_no_data():
    """
    Prueba para is_cached: verifica que devuelve False si los datos no están en caché
    """
    cache = {}
    cache_key = ('Mexico City', 'turista')
    
    assert is_cached(cache, cache_key) == False

def test_is_cached_expired_data():
    """
    Prueba para is_cached: verifica que devuelve False si los datos en caché han expirado
    """
    cache = {}
    cache_key = ('Mexico City', 'turista')
    data = {"weather": "sunny"}
    timestamp = time() - 600  
    cache[cache_key] = (data, timestamp)
    
    assert is_cached(cache, cache_key) == False

def test_store_in_cache():
    """
    Prueba para store_in_cache: verifica que los datos se almacenan correctamente
    """
    cache = {}
    cache_key = ('Mexico City', 'turista')
    data = {"weather": "sunny"}
    
    store_in_cache(cache, cache_key, data)
    
    assert cache[cache_key][0] == data
    assert time() - cache[cache_key][1] < 1