from django.db import models
from apps.soft_delete.model import SoftDeleteModel

class Facultad(SoftDeleteModel):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Carrera(SoftDeleteModel):
    nombre = models.CharField(max_length=200)
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name="carreras")

    def __str__(self):
        return f"{self.nombre} - {self.facultad.nombre}"
