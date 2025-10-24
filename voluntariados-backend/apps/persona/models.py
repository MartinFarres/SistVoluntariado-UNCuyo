from django.db import models
from apps.soft_delete.model import SoftDeleteModel

class Persona(SoftDeleteModel):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
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

    def delete(self, *args, **kwargs):

        if not self.is_active:
            return  # Already inactive, do nothing
    
        # If no user, just delete the persona
        super().delete(*args, **kwargs)

        # Delete related user if exists
        user = getattr(self, 'user', None)
        if user:
            user.delete()

class Voluntario(Persona):
    interno = models.BooleanField(default=False)  # p. ej. es voluntario de la facultad
    observaciones = models.TextField(null=True, blank=True)
    carrera = models.ForeignKey("facultad.Carrera", null=True, blank=True, on_delete=models.SET_NULL)
    class Condicion(models.TextChoices):
        ESTUDIANTE = "Estudiante", "Estudiante"
        DOCENTE = "Docente", "Docente"
        EGRESADO = "Egresado", "Egresado"
        PERSONAL_NO_DOCENTE = "Personal no docente", "Personal no docente"
        INTERCAMBIO = "Intercambio", "Intercambio"

    condicion = models.CharField(max_length=20, choices=Condicion.choices, default=Condicion.ESTUDIANTE)

class Gestionador(Persona):
    pass

class Administrativo(Gestionador):
    pass


class Delegado(Gestionador):

    organizacion = models.ForeignKey(
        "organizacion.Organizacion", null=True, blank=True, on_delete=models.SET_NULL, related_name="delegados" 
    )