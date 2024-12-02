import pytest
from rest_framework.test import APIClient
from rest_framework import status
from ..models import NoteModel

@pytest.mark.django_db
def test_create_note_view():
    # Arrange: Crear un cliente de API y los datos para la nota
    client = APIClient()
    note_data = {
        'title': 'Nota desde Vista',
        'content': 'Este es el contenido de la nota desde la vista'
    }

    # Act: Enviar una solicitud POST a la vista
    response = client.post('/notes/create/', note_data, format='json')

    # Assert: Verificar que la solicitud fue exitosa
    assert response.status_code == status.HTTP_201_CREATED
    assert NoteModel.objects.count() == 1
    assert response.data['title'] == note_data['title']
    assert response.data['content'] == note_data['content']

@pytest.mark.django_db
def test_create_note_view_invalid_data():
    # Arrange: Crear un cliente de API con datos inválidos
    client = APIClient()
    invalid_data = {
        'content': 'Sin título'
    }

    # Act: Enviar una solicitud POST con datos inválidos
    response = client.post('/notes/create/', invalid_data, format='json')

    # Assert: Verificar que la solicitud fue rechazada
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.data
    assert NoteModel.objects.count() == 0
