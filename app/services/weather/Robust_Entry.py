import json
from Levenshtein import ratio

class RobustEntry:

    def __init__(self, city):
        """
        Inicializa una nueva instancia de la clase RobustEntry.
        Args:
        - city (str): El nombre de la ciudad.
        Atributos:
        - self.city (str): El nombre de la ciudad, sin espacios al principio y al final, y convertido a mayúsculas.
        - self.best_match (str): La mejor coincidencia de ciudad encontrada.
        - self.is_valid_city (bool): Un indicador de si la ciudad es válida o no.
        - self.cities_available (list): Una lista de ciudades disponibles cargadas desde el archivo 'Cities.json'.
        - self.iatas_cities_available (dict): Un diccionario de ciudades disponibles cargadas desde el archivo 'Iatas.json'.
        """
        self.city = city.strip().upper()
        self.best_match = None
        self.is_valid_city = False  
        self.cities_available = self.load_json('Cities.json')
        self.iatas_cities_available = self.load_json('Iatas.json')

        if self.city in self.iatas_cities_available:
            self.best_match = self.iatas_cities_available[self.city]
            self.is_valid_city = True

    def load_json(self, filename):
        """Carga y retorna el contenido de un archivo JSON."""
        with open(filename, 'r') as file:
            return json.load(file)



    def get_city_well_written(self):
        """
        Obtiene una versión bien escrita del nombre de la ciudad o sugiere una ciudad si la similitud es alta.
        Retorna:
            dict: Un diccionario con la ciudad bien escrita o una sugerencia.
        """
        if self.city_in_iata():
            return self.city_as_iata()

        return self.find_closest_city()



    def city_in_iata(self):
        """Verifica si la entrada es un código IATA válido."""
        return self.city in self.iatas_cities_available



    def city_as_iata(self):
        """Si la ciudad es un IATA válido, devuelve la ciudad correspondiente."""
        self.is_valid_city = True 
        self.city = self.iatas_cities_available[self.city]
        return {'city': self.city}



    def find_closest_city(self):
        """
        Encuentra la ciudad más cercana en similitud y determina si es válida o si se debe sugerir.
        """
        self.best_match = None
        highest_ratio = 0
        threshold = 0.7

        for available_city in self.cities_available:
            current_ratio = ratio(self.city, available_city.upper())
            if current_ratio > highest_ratio:
                highest_ratio = current_ratio
                self.best_match = available_city

        if highest_ratio > threshold and highest_ratio < 1.0:
            self.is_valid_city = False
            return self.city_suggestion()
        elif highest_ratio == 1.0:
            self.is_valid_city = True
            return {'city': self.best_match}
        else:
            self.is_valid_city = False
            return self.city_not_found()



    def city_suggestion(self):
        """Devuelve una sugerencia cuando la ciudad no es exacta, pero hay una coincidencia cercana."""
        return {
            'suggestion': self.best_match,
            'message': f"La ciudad '{self.city}' no fue encontrada, ¿quisiste decir '{self.best_match}'?"
        }



    def city_not_found(self):
        """Devuelve un mensaje de error cuando no se encuentra ninguna ciudad válida."""
        return {'error': 'La ciudad no existe y/o no se encuentra disponible, intenta con otro nombre.'}



    def get_iata(self):
        """
        Obtiene el código IATA de la ciudad bien escrita.
        Retorna:
        list: Una lista con el código IATA o una lista vacía si no hay coincidencia o si es una sugerencia.
        """
        if self.is_valid_city:
            for iata_code, city_name in self.iatas_cities_available.items():
                if city_name.upper() == self.best_match.upper():
                    return [iata_code]
        return []
