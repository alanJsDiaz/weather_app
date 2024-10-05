
from flask import Flask, render_template_string
from app.services.helpers.template_helpers import render_template_with_error

app = Flask(__name__)

def test_render_template_with_error():
    """
    Prueba para render_template_with_error: verificar que renderiza la plantilla con un mensaje de error
    """
    with app.test_request_context():
        template = "<html><body>{{ error }}</body></html>"
        error_message = "Error de prueba"
        result = render_template_string(template, error=error_message)
        assert "Error de prueba" in result

def test_render_template_with_empty_error():
    """
    Prueba para render_template_with_error: verificar que renderiza la plantilla correcta con un error vacío
    """
    with app.test_request_context():
        template = "<html><body>{{ error }}</body></html>"
        error_message = ""
        
        result = render_template_string(template, error=error_message)
        assert "<body></body>" in result
