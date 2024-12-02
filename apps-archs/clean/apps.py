from django.apps import AppConfig

# Sustituir my_app por el nombre de la app


class App1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ app_name }}"
