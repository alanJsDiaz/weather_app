import json
from Levenshtein import  ratio

class RobustEntry:

    def __init__(self, city):
        """
        Inicializa una nueva instancia de la clase Robust_Entry.
        Args:
        - city (str): El nombre de la ciudad.
        Atributos:
        - self.city (str): El nombre de la ciudad, sin espacios al principio y al final, y convertido a mayúsculas.
        - self.cities_available (list): Una lista de ciudades disponibles cargadas desde el archivo 'Ciudades.json'.
        - self.iatas_cities_available (dict): Un diccionario de ciudades disponibles cargadas desde el archivo 'Iatas.json'.
        """
        self.city = city.strip().upper()
        with open('Cities.json', 'r') as file:
            self.cities_available = json.load(file)
        with open('Iatas.json', 'r') as file:
            self.iatas_cities_available = json.load(file)



    def get_city_well_written(self):
        """
        Obtiene una versión bien escrita del nombre de la ciudad o sugiere una ciudad si la similitud es alta.
        Retorna:
            dict: Un diccionario con la ciudad bien escrita o una sugerencia.
        """
        # Primero verifica si el usuario ingresó un IATA válido
        if self.city in self.iatas_cities_available:
            return {'city': self.iatas_cities_available[self.city]}  # Se encontró la ciudad por IATA
        
        best_match = None
        highest_ratio = 0
        threshold = 0.7  # Umbral de similitud

        # Busca la mejor coincidencia de la ciudad en las ciudades disponibles
        for available_city in self.cities_available:
            current_ratio = ratio(self.city, available_city.upper())
            if current_ratio > highest_ratio:
                highest_ratio = current_ratio
                best_match = available_city

        # Si la similitud es suficientemente alta, sugiere la ciudad
        if highest_ratio > threshold and highest_ratio < 1.0:
            return {
                'suggestion': best_match,
                'message': f"La ciudad '{self.city}' no fue encontrada, ¿quisiste decir '{best_match}'?"
            }
        elif highest_ratio == 1.0:
            return {'city': best_match}  # La ciudad coincide perfectamente
        else:
            return {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}




    def get_iata(self):
        """
        Obtiene la primera IATA de la ciudad.
        Return:
        str: El primer código IATA encontrado o una lista vacía si no hay coincidencia.
        """
        if self.city == 'error':
            return []
        else:
            for iata_code, city_name in self.iatas_cities_available.items():
                if city_name == self.city:
                    return [iata_code]  
            return []