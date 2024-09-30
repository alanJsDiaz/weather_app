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
        Obtiene una versión bien escrita del nombre de la ciudad.
        Retorna:
            str: La versión bien escrita del nombre de la ciudad.
        """
        city_aux = self.city
        self.city = self.iatas_cities_available.get(self.city, self.city)
        if self.city != city_aux:
            return self.city
        best_match = None
        highest_ratio = 0
        threshold = 0.7  
        for available_city in self.cities_available:
            current_ratio = ratio(self.city, available_city.upper())
            if current_ratio > highest_ratio:
                highest_ratio = current_ratio
                best_match = available_city
        if highest_ratio < threshold:
            return 'error'
        else:
            self.city = best_match
            return best_match



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