from ..serializers.generic_serializer import NoteSerializer


def test_note_serializer_validation():
    # Arrange: Datos válidos para crear una nota
    valid_data = {"title": "Título de Prueba", "content": "Contenido de la nota"}

    # Act: Validar los datos usando el serializador
    serializer = NoteSerializer(data=valid_data)
    is_valid = serializer.is_valid()

    # Assert: Verificar que los datos sean válidos
    assert is_valid is True
    assert serializer.validated_data["title"] == valid_data["title"]
    assert serializer.validated_data["content"] == valid_data["content"]


def test_note_serializer_invalid_data():
    # Arrange: Datos inválidos (sin título)
    invalid_data = {"content": "Contenido sin título"}

    # Act: Validar los datos usando el serializador
    serializer = NoteSerializer(data=invalid_data)
    is_valid = serializer.is_valid()

    # Assert: Verificar que los datos no sean válidos
    assert is_valid is False
    assert "title" in serializer.errors
