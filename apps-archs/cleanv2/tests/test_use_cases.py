import pytest
from unittest.mock import Mock
from ..use_cases.generic_use_case import CreateNoteUseCase
from ..core.entities import Note

@pytest.mark.django_db
def test_create_note(mocker):
    # Crear un mock del adaptador
    mock_adapter = Mock()
    mock_adapter.save.return_value = Note(
        title="Test Title",
        content="Test Content",
        created_at="2024-12-04"
    )
    
    # Crear el caso de uso con el mock
    use_case = CreateNoteUseCase(note_adapter=mock_adapter)
    
    # Ejecutar el caso de uso
    result = use_case.execute("Test Title", "Test Content")
    
    # Verificar resultados
    assert result.title == "Test Title"
    assert result.content == "Test Content"
    mock_adapter.save.assert_called_once()
