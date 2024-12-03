# Ejemplo de Uso de Django Injector

Este README proporciona un ejemplo sobre cómo utilizar `django-injector` para manejar la instancia de un adaptador, como en el caso del `CreateNoteUseCase`.

## Instalación de django-injector

Primero, instala `django-injector` usando `pip`:

```bash
pip install django-injector
```

## Configuración del Proyecto para usar django-injector

Una vez instalado, debes configurar `django-injector` en tu proyecto. Agrega `django_injector` a la lista de aplicaciones instaladas en el archivo `settings.py`:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_injector',
    ...
]
```

## Definir el Contenedor de Dependencias

Define un módulo que proporcionará las instancias necesarias. Utilizaremos `Injector` para definir cómo se crean las instancias.

```python
# my_app_module.py
from injector import Module, singleton, provider
from .adapters.generic_adapter import DbNoteAdapter
from .use_cases.create_note_use_case import CreateNoteUseCase

class MyAppModule(Module):
    @singleton
    @provider
    def provide_db_adapter(self) -> DbNoteAdapter:
        return DbNoteAdapter()

    @singleton
    @provider
    def provide_create_note_use_case(self, db_adapter: DbNoteAdapter) -> CreateNoteUseCase:
        return CreateNoteUseCase(note_repository=db_adapter)
```

En este módulo, `MyAppModule` define las reglas para instanciar `DbNoteAdapter` y `CreateNoteUseCase`. La anotación `@provider` le dice a `Injector` cómo crear una instancia, mientras que `@singleton` asegura que se reutilice la misma instancia durante el ciclo de vida de la aplicación.

## Configuración de Injector en apps.py

Luego, modifica el archivo `apps.py` para cargar el módulo de inyección:

```python
# apps.py
from django.apps import AppConfig
from django_injector import singleton

class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'

    def ready(self):
        from injector import Injector
        from .my_app_module import MyAppModule

        injector = Injector([MyAppModule()])
        singleton.set_injector(injector)
```

## Uso del Contenedor de Dependencias en Vistas

Con `django-injector`, puedes inyectar la dependencia del caso de uso directamente en las vistas.

```python
# views.py
from django.http import JsonResponse
from django_injector import inject
from .use_cases.create_note_use_case import CreateNoteUseCase

@inject
def create_note_view(request, create_note_use_case: CreateNoteUseCase):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Ejecutar el caso de uso con la inyección automática de dependencias
        saved_note = create_note_use_case.execute(title, content)

        return JsonResponse({
            "title": saved_note.title,
            "content": saved_note.content,
            "created_at": saved_note.created_at
        })
```

Gracias a `@inject`, `django-injector` se encarga de proporcionar automáticamente la instancia de `CreateNoteUseCase` al método `create_note_view`.

## Beneficios de django-injector

1. **Automatización de la Inyección de Dependencias**: `django-injector` elimina la necesidad de instanciar manualmente cada dependencia y facilita la reutilización.

2. **Desacoplamiento y Testabilidad**: Mantener las dependencias desacopladas del código de lógica ayuda a que las pruebas sean más fáciles de manejar y escribir, ya que puedes cambiar la implementación inyectada sin necesidad de modificar la lógica del caso de uso.

3. **Mantenimiento**: Proporciona una arquitectura más mantenible al reducir la cantidad de código repetitivo relacionado con la creación de instancias.

Este enfoque es particularmente útil en proyectos más grandes o con muchas dependencias donde la automatización de la creación de objetos puede simplificar mucho la vida de los desarrolladores y la escalabilidad del proyecto.

