# Este archivo es para los modelos de la base de datos, de momento no vamosa a guardar nada en nuestra base de datos, no lo usaremos
# Este es para el ejemplo
from django.db import models


class NoteModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
