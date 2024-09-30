import pandas as pd


class Flights:

    def __init__(self):
        """
        Inicializa el objeto Vuelos.
        Parámetros:
        Ninguno
        Retorna:
        Ninguno
        """
        self.cache = {}
        self.df = pd.read_csv('dataset1.csv')



    def get_origin_coordinates(self, origin):
        """
        Recupera las coordenadas de la ciudad de origen.
        Args:
            origin (str): El nombre de la ciudad de origen.
        Returns:
            dict: Un diccionario que contiene la latitud y longitud de la ciudad de origen. Si ocurre un error, el diccionario contendrá una clave 'error' con un mensaje de error.
        """
        try:
            origin_coordinates = self.df[self.df["origin"] == origin][["origin_latitude", "origin_longitude"]].to_dict(orient='records')
            if not origin_coordinates:
                return {'error': f"No se encontraron coordenadas para la ciudad de origen '{origin}'."}
            return origin_coordinates[0]
        except Exception as e:
            return {'error': str(e)}



    def get_destination_coordinates(self, destination):
        """
        Recupera las coordenadas de la ciudad de destino.
        Args:
            destination (str): El nombre de la ciudad de destino.
        Returns:
            dict: Un diccionario que contiene la latitud y longitud de la ciudad de destino. Si ocurre un error, el diccionario contendrá una clave 'error' con un mensaje de error.
        """
        try:
            destination_coordinates = self.df[self.df["destination"] == destination][["destination_latitude", "destination_longitude"]].to_dict(orient='records')        
            if not destination_coordinates:
                return {'error': f"No se encontraron coordenadas para la ciudad de destino '{destination}'."}
            return destination_coordinates[0]
        except Exception as e:
            return {'error': str(e)}



    def get_available_flights_by_destination(self, destination):
        """
        Recupera los vuelos disponibles para un destino
        Args:
            destino (str): El nombre de la ciudad de destino.
        Returns:
            dict: Un diccionario que contiene los vuelos disponibles para el origen y destino dados. Si ocurre un error, el diccionario contendrá una clave 'error' con un mensaje de error.
        """
        available_flights = self.df[self.df["destination"].isin(destination)].to_dict(orient='records')
        return available_flights



    def get_available_flights_by_origin(self, iata):
        """
        Recupera los vuelos disponibles para un origen
        Args:
            origen (str): El nombre de la ciudad de origen.
        Returns:
            dict: Un diccionario que contiene los vuelos disponibles para el origen y destino dados. Si ocurre un error, el diccionario contendrá una clave 'error' con un mensaje de error.
        """
        available_flights = self.df[self.df["origin"].isin(iata)].to_dict(orient='records')
        return available_flights







