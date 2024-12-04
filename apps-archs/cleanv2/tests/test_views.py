import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateNoteView:
    def test_create_note_view(self):
        # Crear cliente de prueba
        client = APIClient()

        # Datos de prueba
        note_data = {
            "title": "Nota de Prueba",
            "content": "Contenido de la nota de prueba",
        }

        # Realizar solicitud POST
        response = client.post("/notes/create/", note_data, format="json")

        # Verificar respuesta
        assert response.status_code == 201
        assert response.data["title"] == "Nota de Prueba"
