
import pytest
from unittest.mock import mock_open, patch
from app.services.helpers.ticket_helpers import generate_ticket, save_ticket_to_csv, search_ticket_in_csv

def test_generate_ticket():
    """
    Prueba para generate_ticket: verificar que genera el código alfanumérico correcto
    """
    ticket = generate_ticket('Mexico City', 'New York')
    assert len(ticket) == 6
    assert ticket.isalnum()

@patch('builtins.open', new_callable=mock_open)
@patch('csv.writer')
def test_save_ticket_to_csv(mock_writer, mock_open_file):
    """
    Prueba para save_ticket_to_csv: verificar que los datos del ticket se guardan correctamente en CSV
    """
    save_ticket_to_csv('Mexico City', 'New York', 'ABC123')
    
    mock_open_file.assert_called_once_with('tickets.csv', mode='a', newline='')
    
    mock_writer.return_value.writerow.assert_called_once_with(['Mexico City', 'New York', 'ABC123'])

@patch('builtins.open', new_callable=mock_open, read_data='Mexico City,New York,ABC123')
@patch('csv.reader')
def test_search_ticket_in_csv(mock_reader, mock_open_file):
    """
    Prueba para search_ticket_in_csv: verificar que se puede buscar un ticket existente en el CSV
    """
    mock_reader.return_value = [['Mexico City', 'New York', 'ABC123']]
    
    origin, destination = search_ticket_in_csv('ABC123')
    
    mock_open_file.assert_called_once_with('tickets.csv', mode='r')
    
    assert origin == 'Mexico City'
    assert destination == 'New York'

@patch('builtins.open', new_callable=mock_open, read_data='Mexico City,New York,ABC123')
@patch('csv.reader')
def test_search_ticket_in_csv_ticket_not_found(mock_reader, mock_open_file):
    """
    Prueba para search_ticket_in_csv: verificar el manejo de errores si el ticket no existe
    """
    mock_reader.return_value = [['Mexico City', 'New York', 'ABC123']]
    
    result = search_ticket_in_csv('DEF456')
    
    assert result == (None, None)
