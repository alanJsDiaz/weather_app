# Sitio web de clima en tiempo real

Este proyecto es un sitio web que consulta en tiempo real el clima y otros datos geográficos de la ciudad de interés del usuario, además puede consultar información acerca de los vuelos relacionados a esta ciudad, es un proyecto pensando para usarse en un aeropuerto.

## Requisitos

Asegúrate de tener instalado Python 3.7 o superior y virtualenv antes de continuar.

## Instalación

1. Clona el repositorio en tu máquina local:
>   git clone https://github.com/alanJsDiaz/weather_app.git

2. Navega al directorio del proyecto:
>   cd weather_app

3. Crea el entorno virtual:
>   python -m venv venv

4. Activa el entorno virtual:
>   source venv/bin/activate

5. Instala las dependencias utilizando requirements.txt:
>   pip install -r requirements.txt

# Ejecución del Programa

Para correr el programa, con el entorno virtual activado, ejecuta el siguiente comando en la terminal desde la raíz del proyecto:

>   python run.py

copia  "url" que se muestra en la terminal , justo despues de haber ejecutado el comando anterior y pegala en tu navegador.

# Ejecución de los Test's
Para correr los tests, con el entorno virtual activado, ejecuta el siguiente comando en la terminal desde la raíz del proyecto:
>   PYTHONPATH=./ pytest

## Extras

1. Contraseñas de los roles 'Sobrecargo' y 'Piloto'
>   Para 'Sobrecargo' usa la contraseña: sobrecargo123
>   Para 'Piloto' usa la contraseña: piloto123