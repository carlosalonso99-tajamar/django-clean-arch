**Principio de Inversión de Dependencias y Ejemplo en Python**

### Paso 1: Definir una Abstracción para la Persistencia
Primero, necesitamos definir una abstracción para nuestro adaptador de persistencia, es decir, una interfaz que cualquier adaptador concreto de almacenamiento deberá implementar. En Python, puedes hacer esto con una clase base abstracta o una interfaz.

Vamos a crear una interfaz llamada `NoteRepository`:

```python
from abc import ABC, abstractmethod
from typing import Protocol

class NoteRepository(Protocol):
    @abstractmethod
    def save(self, note: "Note") -> "Note":
        pass
```

Esta interfaz define el método `save` que deberá implementar cualquier clase de persistencia de notas.

### Paso 2: Modificar el Caso de Uso para Inyectar Dependencias
Vamos a modificar el `CreateNoteUseCase` para que dependa de esta abstracción (`NoteRepository`) y no de una implementación concreta (`DbNoteAdapter`). Esto se hace generalmente mediante inyección de dependencias, lo cual permite pasar el adaptador al caso de uso como un parámetro.

```python
from datetime import datetime

class CreateNoteUseCase:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    def execute(self, title: str, content: str) -> "Note":
        # Crear la entidad de nota con la lógica de negocio aplicada
        note = Note(title=title, content=content, created_at=datetime.now())

        # Usar el repositorio (a través de la abstracción) para guardar la nota
        saved_note = self.note_repository.save(note)
        
        return saved_note
```

### Paso 3: Crear Implementación del Repositorio
Ahora puedes implementar un adaptador concreto que use una base de datos para guardar las notas. Esto sería la implementación concreta que cumple con la interfaz `NoteRepository`:

```python
class DbNoteAdapter(NoteRepository):
    def save(self, note: "Note") -> "Note":
        note_instance = NoteModel.objects.create(
            title=note.title,
            content=note.content,
            created_at=note.created_at
        )
        return note
```

### Paso 4: Instanciar e Inyectar Dependencias
Finalmente, en el código donde necesites usar el `CreateNoteUseCase`, puedes pasarle la implementación concreta del adaptador que deseas utilizar. De esta forma, el caso de uso no está acoplado a ninguna implementación específica del almacenamiento.

```python
# Instanciar el adaptador concreto
db_adapter = DbNoteAdapter()

# Inyectar el adaptador al caso de uso
create_note_use_case = CreateNoteUseCase(note_repository=db_adapter)

# Ejecutar el caso de uso
note = create_note_use_case.execute("Mi Título", "Contenido de la nota")
```

### Ventajas de Aplicar Inversión de Dependencias

- **Desacoplamiento**: `CreateNoteUseCase` ahora está desacoplado de la implementación concreta de la persistencia, lo que hace que el código sea más flexible y fácil de cambiar. Puedes cambiar la implementación concreta sin cambiar el código del caso de uso.
- **Pruebas**: Al inyectar la dependencia, puedes pasar un "mock" del repositorio en lugar del adaptador concreto durante las pruebas, lo cual facilita los tests unitarios.
- **Sustituibilidad**: Puedes crear otras implementaciones del `NoteRepository` para, por ejemplo, guardar las notas en una base de datos diferente o incluso en un archivo, y el caso de uso no tendrá que cambiar en absoluto.

### Ejemplo Concreto: Cambio de Base de Datos y Pruebas

**Imagina que tienes la aplicación de notas en producción y decides hacer algunos cambios.**

- **Cambiar la Base de Datos de SQLite a MongoDB**: La empresa decide que para soportar el creciente número de usuarios, la base de datos debería ser MongoDB en lugar de SQLite. Como tienes el `CreateNoteUseCase` desacoplado de la implementación específica del almacenamiento, este cambio será mucho más sencillo.

- **Pruebas Unitarias Simples**: Supongamos que estás probando la lógica de tu `CreateNoteUseCase`. En lugar de probar directamente contra la base de datos (lo cual sería más lento y dependiente de un recurso externo), puedes crear un "mock" o una implementación en memoria del `NoteRepository` para usar en los tests.

### Paso 1: Implementación Alternativa del NoteRepository
Para demostrar el poder de este desacoplamiento, crearemos una segunda implementación del `NoteRepository`, esta vez utilizando MongoDB como almacenamiento.

```python
class MongoNoteAdapter(NoteRepository):
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def save(self, note: "Note") -> "Note":
        note_data = {
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
        }
        self.mongo_client.notes.insert_one(note_data)
        return note
```

Aquí tenemos una clase `MongoNoteAdapter` que guarda la nota en MongoDB en lugar de en una base de datos SQL. El `CreateNoteUseCase` no necesita ningún cambio. Sólo tendrás que pasarle esta nueva implementación del repositorio cuando la uses.

### Paso 2: Pruebas Unitarias con Mocking
Ahora, vamos a ver cómo hacer que las pruebas unitarias de `CreateNoteUseCase` sean más rápidas y menos dependientes de recursos externos. Utilizaremos una implementación en memoria para simular el repositorio.

```python
class InMemoryNoteRepository(NoteRepository):
    def __init__(self):
        self.notes = []

    def save(self, note: "Note") -> "Note":
        self.notes.append(note)
        return note
```

Luego puedes usar este repositorio para probar el `CreateNoteUseCase`:

```python
def test_create_note():
    # Crear un repositorio en memoria para las pruebas
    repository = InMemoryNoteRepository()
    use_case = CreateNoteUseCase(note_repository=repository)

    # Ejecutar el caso de uso
    note = use_case.execute("Mi Título", "Contenido de la nota")

    # Verificar que la nota se ha guardado
    assert note in repository.notes
    assert note.title == "Mi Título"
    assert note.content == "Contenido de la nota"
```

### Qué Conseguimos

- **Cambio de Almacenamiento sin Modificar la Lógica del Caso de Uso**: Imagina que ahora, en lugar de usar SQLite, se necesita cambiar a MongoDB para soportar una escala mayor. Gracias a que `CreateNoteUseCase` depende de una abstracción (`NoteRepository`), simplemente puedes crear una implementación del repositorio para MongoDB e inyectarla en el caso de uso. No tienes que cambiar ninguna línea del `CreateNoteUseCase`, solo el código donde se instancia el repositorio.

- **Pruebas Unitarias sin Dependencias Externas**: Como `CreateNoteUseCase` no depende directamente de la base de datos, puedes pasar una implementación "mock" del `NoteRepository` durante las pruebas. Esto hace que las pruebas sean más rápidas (no necesitas una base de datos real) y menos frágiles (no se rompen por problemas de conexión).

- **Facilidad de Extensión**: Supongamos que en el futuro decides agregar almacenamiento en la nube (por ejemplo, Amazon S3) para tus notas o un caché temporal. Solo necesitas crear una nueva implementación de `NoteRepository` que guarde la información en Amazon S3, y después pasar esa implementación a `CreateNoteUseCase` sin cambiar nada de la lógica de negocio.

- **Separación de Responsabilidades**: La lógica de negocio (crear una nota) está separada de los detalles de almacenamiento (dónde y cómo se guarda la nota). Esto sigue el principio de "separación de preocupaciones", haciendo que el código sea más limpio y fácil de mantener.

### Resumen
La Inversión de Dependencias te permite:

- Cambiar la implementación del almacenamiento sin afectar la lógica de negocio.
- Hacer que las pruebas unitarias sean más rápidas y fáciles de configurar.
- Escalar y extender el sistema con nuevas formas de persistencia sin cambios en la lógica de los casos de uso.
- Reducir el acoplamiento y aumentar la reutilización del código.

