from django.db import models
from apps.soft_delete.model import SoftDeleteModel

class Organizacion(SoftDeleteModel):
    nombre = models.CharField(max_length=200,unique=True)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(null=True, blank=True)
    contacto_email = models.EmailField(null=True, blank=True)
    localidad = models.ForeignKey("ubicacion.Localidad", null=True, blank=True, on_delete=models.SET_NULL)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("nombre",)
        indexes = [
            models.Index(fields=["nombre"]),
        ]

    def __str__(self):
        return self.nombre
