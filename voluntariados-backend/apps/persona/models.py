from django.db import models
from apps.soft_delete.model import SoftDeleteModel

class Persona(SoftDeleteModel):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    localidad = models.ForeignKey(
        "ubicacion.Localidad", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ("apellido", "nombre")
        indexes = [
            models.Index(fields=["dni"]),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni or 'sin DNI'})"


class Voluntario(Persona):
    interno = models.BooleanField(default=False)  # p. ej. es voluntario de la facultad
    observaciones = models.TextField(null=True, blank=True)
    carrera = models.ForeignKey("facultad.Carrera", null=True, blank=True, on_delete=models.SET_NULL)

class Gestionador(Persona):
    pass

class Administrativo(Gestionador):
    pass


class Delegado(Gestionador):

    organizacion = models.ForeignKey(
        "organizacion.Organizacion", null=True, blank=True, on_delete=models.SET_NULL, related_name="delegados" 
    )