from django.db import models
from django.contrib.auth import get_user_model

class Negocios(models.Model):
    nombre = models.CharField(max_length=50)
    dueño = models.ForeignKey(get_user_model(), related_name="negocios", on_delete=models.CASCADE)
    transbank = models.CharField(max_length=200)
    efectivo = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
