from django.db import models

class Voluntario(models.Model):
    persona = models.OneToOneField("personas.Persona", on_delete=models.CASCADE, related_name="voluntarios")
    fecha_alta = models.DateField(auto_now_add=True)
    interno = models.BooleanField(default=False)  # p. ej. es voluntario de la facultad
    observaciones = models.TextField(null=True, blank=True)
    carrera = models.ForeignKey("facultad.Carrera", null=True, blank=True, on_delete=models.SET_NULL)
    activo = models.BooleanField(default=True) # (?? checkar si es necesario)

    def __str__(self):
        return f"Voluntario: {self.persona}"
