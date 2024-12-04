from injector import Module, singleton, provider
from .adapters.generic_adapter import DbNoteAdapter, NoteAdapter
from .use_cases.generic_use_case import CreateNoteUseCase

class MyAppModule(Module):
    @singleton
    @provider
    def provide_db_adapter(self) -> NoteAdapter:
        return DbNoteAdapter()

    @singleton
    @provider
    def provide_create_note_use_case(self, db_adapter: NoteAdapter) -> CreateNoteUseCase:
        return CreateNoteUseCase(note_adapter=db_adapter)
