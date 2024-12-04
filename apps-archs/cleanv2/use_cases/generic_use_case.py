from datetime import datetime
from ..core.entities import Note
from ..adapters.generic_adapter import NoteAdapter

class CreateNoteUseCase:
    def __init__(self, note_adapter: NoteAdapter):
        self.note_adapter = note_adapter
    
    def execute(self, title: str, content: str) -> Note:
        # Crear la entidad de nota con la lógica de negocio aplicada
        note = Note(title=title, content=content, created_at=datetime.now())
        # Persistir la entidad usando el adaptador
        saved_note = self.note_adapter.save(note)
        return saved_note
