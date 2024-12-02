### README - Flujo de Capas en Clean Architecture para Crear una Nota

#### Introducción
Este documento describe el flujo de la arquitectura Clean utilizada en una aplicación Django REST Framework (DRF) para implementar una funcionalidad sencilla: crear una nota. La arquitectura sigue principios de separación de responsabilidades, manteniendo una lógica de negocio limpia y desacoplada del framework y de la infraestructura.

#### Resumen de la Funcionalidad
La funcionalidad que desarrollamos permite crear una nota, almacenándola en una base de datos, y devolver una respuesta con la información de la nota creada. Los datos principales son:

- **Título (title)**: El título de la nota.
- **Contenido (content)**: El contenido de la nota.
- **Fecha de creación (created_at)**: La fecha y hora de la creación de la nota.

#### Capas Involucradas y Flujo
El flujo de las capas y su interacción se detallan a continuación:

1. **Cliente Envía Solicitud (HTTP POST):**
   - El proceso comienza cuando el cliente envía una solicitud HTTP POST con los datos de la nota (title, content) al endpoint de la API.

2. **Capa de Vistas (views) Recibe la Solicitud:**
   - **Vista (CreateNoteView):**
     - La vista actúa como el punto de entrada de la solicitud. Recibe los datos y utiliza un serializador para validar la estructura y el contenido de la solicitud.
     - Si los datos son válidos, la vista delega la lógica de negocio al caso de uso correspondiente (CreateNoteUseCase).

3. **Capa de Serializadores (serializers) Valida los Datos:**
   - **Serializador (NoteSerializer):**
     - El serializador se asegura de que los datos recibidos (title y content) cumplen con las reglas de validación, tales como longitud o formato requerido.
     - Si los datos no son válidos, la vista devuelve un error 400 Bad Request al cliente.

4. **Capa de Casos de Uso (use_cases) Procesa la Lógica de Negocio:**
   - **Caso de Uso (CreateNoteUseCase):**
     - El caso de uso es responsable de la lógica de negocio. Crea una entidad de tipo Note con los datos proporcionados.
     - El caso de uso utiliza el adaptador (DbNoteAdapter) para almacenar la nota en la base de datos, manteniendo así la lógica de negocio desacoplada de la infraestructura.

5. **Capa de Adaptadores (adapters) Interactúa con la Base de Datos:**
   - **Adaptador (DbNoteAdapter):**
     - El adaptador convierte la entidad Note a una instancia del modelo de Django (NoteModel) y la persiste en la base de datos.
     - Esta capa es la encargada de abstraer la lógica específica de almacenamiento, para que el caso de uso no necesite saber cómo interactuar con la base de datos.

6. **Capa de Casos de Uso Devuelve la Nota:**
   - **Nota Guardada Devuelta por el Caso de Uso:**
     - El adaptador devuelve la entidad Note almacenada, y el caso de uso la pasa a la capa de vistas.

7. **Capa de Vistas (views) Devuelve la Respuesta:**
   - **Vista (CreateNoteView):**
     - La vista construye una respuesta HTTP con la información de la nota (title, content, created_at) y la devuelve al cliente con un estado 201 Created.

#### Beneficios del Flujo en Clean Architecture
- **Desacoplamiento**: Cada capa tiene una responsabilidad específica, lo que facilita la mantenibilidad y la extensibilidad del sistema.
- **Testabilidad**: Al mantener la lógica de negocio en los casos de uso y desacoplarla de la infraestructura, podemos probar cada capa de manera independiente, usando adaptadores simulados (mocks) si es necesario.
- **Flexibilidad**: Cambiar la implementación de una capa, como la de persistencia (base de datos), solo requiere modificar el adaptador, mientras que el resto del sistema permanece intacto.

#### Relación entre las Capas
- **Vistas (views)**: Actúan como controladores, manejan la solicitud y la respuesta del cliente.
- **Serializadores (serializers)**: Validan los datos de entrada y aseguran que cumplen con los requisitos antes de delegarlos a la lógica de negocio.
- **Casos de Uso (use_cases)**: Son responsables de la lógica de negocio, orquestando el flujo necesario para completar la acción requerida.
- **Adaptadores (adapters)**: Interactúan con sistemas externos, como la base de datos, asegurando que la lógica de negocio permanezca libre de detalles de infraestructura.
- **Entidad (core)**: Define las entidades del dominio sin ningún conocimiento sobre cómo se almacenan o cómo son gestionadas por el sistema.

#### Conclusión
El flujo de la arquitectura Clean en Django para crear una nota asegura que cada capa tiene una única responsabilidad, lo que contribuye a un código modular y limpio. Esta estructura hace que el sistema sea fácil de mantener, escalar y probar, gracias al desacoplamiento entre la lógica de negocio y la infraestructura.

Este ejemplo básico de la funcionalidad de creación de una nota ayuda a ilustrar cómo las diferentes capas se comunican y colaboran para manejar una solicitud, desde la entrada del cliente hasta la persistencia y la respuesta.

