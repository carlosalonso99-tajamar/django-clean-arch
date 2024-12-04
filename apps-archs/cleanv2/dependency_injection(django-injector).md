# Django Injector Setup

`django-injector` es un complemento que permite agregar la funcionalidad de inyección de dependencias a tu proyecto Django, basado en el framework `Injector`. Esta guía te ayudará a configurar y utilizar `django-injector` de manera efectiva en tu aplicación Django.

## Requisitos Previos

- Python 3.7+
- Django 2.2+
- `django-injector` compatible con Django Rest Framework (opcional)

## Instalación

Para instalar `django-injector`, usa el siguiente comando:

```bash
pip install django_injector
```

## Configuración en `settings.py`

1. **Agrega `django_injector` a `INSTALLED_APPS`:**

   ```python
   INSTALLED_APPS = [
       ...
       'django_injector',
   ]
   ```

2. **Configura los módulos de inyección:**

   Define los módulos que quieres utilizar con `INJECTOR_MODULES` en `settings.py`:

   ```python
   INJECTOR_MODULES = [
       'notes.modules.MyAppModule',  # Reemplaza con la ruta a tu módulo
   ]
   ```

## Crear un Módulo de Inyección

Un módulo define cómo se crean las dependencias. Por ejemplo, crea un archivo `modules.py` dentro de tu aplicación:

```python
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
```

Este módulo define cómo crear instancias de `NoteAdapter` y `CreateNoteUseCase`.

## Usar Inyección en una Vista

Para utilizar las dependencias en una vista, agrega el decorador `@inject` desde el paquete `injector`.

Por ejemplo, en una vista basada en clases:

```python
from injector import inject
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .use_cases.generic_use_case import CreateNoteUseCase
from .serializers.generic_serializer import NoteSerializer

class CreateNoteView(APIView):
    @inject
    def __init__(self, create_note_use_case: CreateNoteUseCase, **kwargs):
        super().__init__(**kwargs)
        self.create_note_use_case = create_note_use_case

    def post(self, request):
        # Validar la entrada usando el serializador
        serializer = NoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Delegar la lógica al caso de uso
        title = serializer.validated_data['title']
        content = serializer.validated_data['content']
        note = self.create_note_use_case.execute(title=title, content=content)

        # Retornar la respuesta
        return Response(
            {'title': note.title, 'content': note.content, 'created_at': note.created_at},
            status=status.HTTP_201_CREATED,
        )
```

## Ejecutar el Proyecto

Con todas las configuraciones listas, puedes ejecutar tu proyecto con:

```bash
python manage.py runserver
```

`django-injector` se encargará de la inyección de dependencias automáticamente.

## Ejemplo de Prueba

Para realizar pruebas con `django-injector`, puedes usar el decorador `@pytest.mark.django_db` para habilitar la base de datos y verificar que tus dependencias se inyecten correctamente. Ejemplo:

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateNoteView:
    def test_create_note_view(self):
        client = APIClient()
        note_data = {
            "title": "Nota de Prueba",
            "content": "Contenido de la nota de prueba",
        }
        response = client.post("/notes/create/", note_data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Nota de Prueba"
```

## Resumen

- `django-injector` facilita la inyección de dependencias en vistas y otros componentes de Django.
- Define tus módulos de inyección y configúuralos en `settings.py`.
- Usa el decorador `@inject` para inyectar dependencias en tus vistas o clases.

Con esto deberías tener una implementación básica y funcional de `django-injector` en tu proyecto. ¡Espero que te sea de ayuda! 😊

