from django.db import models
from apps.soft_delete.model import SoftDeleteModel

class Organizacion(SoftDeleteModel):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    contacto_email = models.EmailField(null=True, blank=True)
    contacto_persona = models.ForeignKey("persona.Persona", null=True, blank=True, on_delete=models.SET_NULL, related_name="organizaciones_contacto")
    localidad = models.ForeignKey("ubicacion.Localidad", null=True, blank=True, on_delete=models.SET_NULL)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre
