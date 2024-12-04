from ..core.entities import Note
from ..models import NoteModel
from typing import Protocol

class NoteAdapter(Protocol):
    def save(self, note: Note) -> Note:
        pass

class DbNoteAdapter(NoteAdapter):
    def save(self, note: Note) -> Note:
        # Guardar la entidad Note en la base de datos usando el modelo de Django
        note_instance = NoteModel.objects.create(
            title=note.title, content=note.content, created_at=note.created_at
        )
        return Note(
            title=note_instance.title,
            content=note_instance.content,
            created_at=note_instance.created_at,
        )
