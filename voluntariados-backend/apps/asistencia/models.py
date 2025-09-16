from django.db import models
from django.conf import settings
from apps.soft_delete.model import SoftDeleteModel

class Asistencia(SoftDeleteModel):
    inscripcion = models.OneToOneField("voluntariado.InscripcionTurno", on_delete=models.CASCADE, related_name="asistencia")
    presente = models.BooleanField(default=False)
    horas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    registrada_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    registrada_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Asistencia {self.inscripcion} - {'Presente' if self.presente else 'Ausente'}"
