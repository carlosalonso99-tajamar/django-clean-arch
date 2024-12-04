from django.urls import path
from .views.generic_view import CreateNoteView

urlpatterns = [
    path("create/", CreateNoteView.as_view() , name="create_note"),
]


# TODO: Revisar si algunos objetos en los que derivan la responsabilidad las capas hay que crearlos (en el init, por parametro o en el metodo)
# TODO: reajustar la plantilla
