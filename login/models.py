from django.db import models
from django.contrib.auth import get_user_model

class Rutas(models.Model):
    usuario = models.ForeignKey(get_user_model(), related_name="rutas", on_delete=models.CASCADE)
    master = models.CharField(max_length=200)
    cache = models.CharField(max_length=200)

    def __str__(self):
        return self.usuario.username
