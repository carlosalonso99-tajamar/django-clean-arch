from ..core.entities import Note
from datetime import datetime


def test_create_note_entity():
    # Arrange & Act: Crear una nueva entidad Note
    title = "Mi Primera Nota"
    content = "Este es el contenido de mi primera nota"
    created_at = datetime.now()
    note = Note(title=title, content=content, created_at=created_at)

    # Assert: Verificar los valores de la entidad
    assert note.title == title
    assert note.content == content
    assert note.created_at == created_at
