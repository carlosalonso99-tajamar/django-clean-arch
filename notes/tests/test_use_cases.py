import pytest
from ..use_cases.generic_use_case import CreateNoteUseCase


@pytest.mark.django_db
def test_create_note():
    use_case = CreateNoteUseCase()
    note = use_case.execute("Mi Título", "Contenido de la nota")
    assert note.title == "Mi Título"
    assert note.content == "Contenido de la nota"
