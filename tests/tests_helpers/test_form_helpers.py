from flask import Flask, request
from app.services.helpers.form_helpers import get_form_data, validate_form_data

app = Flask(__name__)

def test_get_form_data():
    """
    Prueba para get_form_data: verificar que los datos se extraen correctamente
    """
    with app.test_request_context('/submit', method='POST', data={'city': 'Mexico City', 'user_type': 'turista', 'password': '1234'}):
        city, user_type, password = get_form_data()
        assert city == 'Mexico City'
        assert user_type == 'turista'
        assert password == '1234'

def test_validate_form_data_missing_city_or_user_type():
    """
    Prueba para validate_form_data: verificar que se muestra un error si faltan la ciudad o el tipo de usuario
    """
    error = validate_form_data('', 'turista', '1234', {})
    assert error == "Por favor, ingresa una ciudad y selecciona un tipo de usuario."

    error = validate_form_data('Mexico City', '', '1234', {})
    assert error == "Por favor, ingresa una ciudad y selecciona un tipo de usuario."

def test_validate_form_data_missing_password():
    """
    Prueba para validate_form_data: verificar que se muestra un error si falta la contraseña para sobrecargo o piloto
    """
    error = validate_form_data('Mexico City', 'sobrecargo', '', {})
    assert error == "Por favor, ingresa la contraseña para sobrecargo."

def test_validate_form_data_incorrect_password():
    """
    Prueba para validate_form_data: verificar que se muestra un error si la contraseña es incorrecta
    """
    USER_PASSWORDS = {'sobrecargo': 'correct_password'}
    error = validate_form_data('Mexico City', 'sobrecargo', 'wrong_password', USER_PASSWORDS)
    assert error == "Contraseña incorrecta. Intenta de nuevo."

def test_validate_form_data_success():
    """
    Prueba para validate_form_data: verificar que no se devuelve ningún error cuando los datos son correctos
    """
    USER_PASSWORDS = {'sobrecargo': 'correct_password'}
    error = validate_form_data('Mexico City', 'sobrecargo', 'correct_password', USER_PASSWORDS)
    assert error is None
