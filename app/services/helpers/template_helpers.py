from flask import render_template

def render_template_with_error(template, error_message):
    """
    Renderiza una plantilla e inserta un mensaje de error.
    """
    return render_template(template, error=error_message)
