from datetime import datetime
from ..core.entities import Note
from ..adapters.generic_adapter import DbNoteAdapter

class CreateNoteUseCase:
    def execute(self, title: str, content: str) -> Note:
        # Crear la entidad de nota con la lógica de negocio aplicada
        note = Note(title=title, content=content, created_at=datetime.now())
        # Aquí podríamos incluir lógica adicional (como validaciones específicas)
        # Llamar al adaptador para persistir la entidad
        db_adapter = DbNoteAdapter()
        
        saved_note = db_adapter.save(note)
        return saved_note
