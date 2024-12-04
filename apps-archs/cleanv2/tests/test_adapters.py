import pytest
from ..adapters.generic_adapter import DbNoteAdapter
from ..core.entities import Note
from ..models import NoteModel
from datetime import datetime


@pytest.mark.django_db
def test_save_note():
    # Arrange: Crear una instancia del adaptador y una entidad Note
    adapter = DbNoteAdapter()
    note = Note(
        title="Nota de Prueba",
        content="Este es el contenido de la nota de prueba",
        created_at=datetime.now(),
    )

    # Act: Guardar la nota usando el adaptador
    saved_note = adapter.save(note)

    # Assert: Verificar que la nota fue guardada correctamente
    assert NoteModel.objects.count() == 1
    assert saved_note.title == note.title
    assert saved_note.content == note.content
    assert isinstance(saved_note, Note)
