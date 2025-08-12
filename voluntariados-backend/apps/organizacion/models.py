from django.db import models

class Organizacion(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    contacto_email = models.EmailField(null=True, blank=True)
    contacto_persona = models.ForeignKey("personas.Persona", null=True, blank=True, on_delete=models.SET_NULL)
    localidad = models.ForeignKey("ubicacion.Localidad", null=True, blank=True, on_delete=models.SET_NULL)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
