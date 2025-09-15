from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    localidad = models.ForeignKey(
        "ubicacion.Localidad", null=True, blank=True, on_delete=models.SET_NULL, related_name="personas"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("apellido", "nombre")
        indexes = [
            models.Index(fields=["dni"]),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni or 'sin DNI'})"


class Voluntario(models.Model):
    fecha_alta = models.DateField(auto_now_add=True)
    interno = models.BooleanField(default=False)  # p. ej. es voluntario de la facultad
    observaciones = models.TextField(null=True, blank=True)
    carrera = models.ForeignKey("facultad.Carrera", null=True, blank=True, on_delete=models.SET_NULL)
    activo = models.BooleanField(default=True) # (?? checkar si es necesario)

    def __str__(self):
        return f"Voluntario: {self.persona}"