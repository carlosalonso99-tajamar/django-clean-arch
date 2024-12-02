# Ruta donde se almacenará la plantilla (ajusta esta variable según tu necesidad)
$basePath = "clean"

# Lista de carpetas y archivos a crear
$estructura = @(
    "__init__.py",
    "apps.py",  # Configuración de la app para Django
    "admin.py", # Registro de modelos en el admin de Django (vacío para personalización)
    "models.py", # Definición de modelos (vacío inicialmente)
    "core\__init__.py",  # Esta capa define las entidades fundamentales del dominio, representando la lógica de negocio pura, sin dependencias externas.
    "core\entities.py", # Base para las entidades del dominio (sin lógica específica)
    "use_cases\__init__.py", # Contiene la lógica de los casos de uso. Orquesta cómo se manipulan las entidades para cumplir con los requisitos de negocio.
    "use_cases\generic_use_case.py", # Caso de uso genérico (nombre base para personalizar)
    "adapters\__init__.py", # Proporciona adaptadores para interactuar con sistemas externos, desacoplando la lógica de negocio de detalles de implementación.
    "adapters\generic_adapter.py", # Adaptador genérico para futuras conexiones (API, etc.)
    "serializers\__init__.py", # Define los serializadores, encargados de convertir las entidades en un formato adecuado para ser expuesto a través de APIs.
    "serializers\generic_serializer.py", # Serializer básico (vacío)
    "views\__init__.py", # Contiene las vistas que manejan la interacción con el cliente mediante APIs, delegando la lógica de negocio a los casos de uso.
    "views\generic_view.py", # Vista de ejemplo con DRF (vacía para personalización)
    "urls.py", # Definición de rutas (vacío para inicializar)
    "tests\__init__.py",
    "tests\test_entities.py", # Pruebas unitarias para las entidades.
    "tests\test_use_cases.py", # Pruebas para los casos de uso.
    "tests\test_adapters.py", # Pruebas para los adaptadores.
    "tests\test_serializers.py", # Pruebas para los serializadores.
    "tests\test_views.py", # Pruebas para las vistas.
    "migrations\__init__.py" # Archivo para inicializar la carpeta de migraciones
)

# Crear las carpetas y archivos
foreach ($item in $estructura) {
    $rutaCompleta = Join-Path -Path $basePath -ChildPath $item
    $directorio = Split-Path -Path $rutaCompleta -Parent

    # Crear la carpeta si no existe
    if (-not (Test-Path -Path $directorio)) {
        New-Item -Path $directorio -ItemType Directory
    }

    # Crear el archivo si no existe y escribir comentarios en __init__.py
    if (-not (Test-Path -Path $rutaCompleta)) {
        New-Item -Path $rutaCompleta -ItemType File

        # Añadir comentarios de descripción a los archivos __init__.py
        if ($item -like "*__init__.py") {
            switch -Wildcard ($item) {
                "core\__init__.py" {
                    Add-Content -Path $rutaCompleta -Value "# Esta capa define las entidades fundamentales del dominio, representando la lógica de negocio pura, sin dependencias externas. Es utilizada por la capa de Casos de Uso (use_cases) para manipular la lógica de negocio."
                }
                "use_cases\__init__.py" {
                    Add-Content -Path $rutaCompleta -Value "# Contiene la lógica de los casos de uso. Orquesta cómo se manipulan las entidades para cumplir con los requisitos de negocio. Llama a la capa de Core (core) para ejecutar la lógica y se invoca desde la capa de Vistas (views)."
                }
                "adapters\__init__.py" {
                    Add-Content -Path $rutaCompleta -Value "# Proporciona adaptadores para interactuar con sistemas externos, desacoplando la lógica de negocio de detalles de implementación. Esta capa es utilizada por los Casos de Uso (use_cases) para interactuar con APIs externas o servicios."
                }
                "serializers\__init__.py" {
                    Add-Content -Path $rutaCompleta -Value "# Define los serializadores, encargados de convertir las entidades en un formato adecuado para ser expuesto a través de APIs. Los serializadores son llamados por la capa de Vistas (views) para validar y transformar los datos."
                }
                "views\__init__.py" {
                    Add-Content -Path $rutaCompleta -Value "# Contiene las vistas que manejan la interacción con el cliente mediante APIs, delegando la lógica de negocio a los Casos de Uso (use_cases). Llama a los Serializadores (serializers) para validar y transformar los datos antes de pasar la información."
                }
                "tests\__init__.py" {
                    Add-Content -Path $rutaCompleta -Value "# Contiene las pruebas unitarias para verificar el correcto funcionamiento de cada componente. Incluye pruebas para entidades, casos de uso, adaptadores, serializadores y vistas."
                }
            }
        }
    }
}

Write-Output "Estructura de plantilla generada exitosamente en $basePath"
