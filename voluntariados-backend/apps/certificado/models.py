from django.db import models
from apps.soft_delete.model import SoftDeleteModel

class Certificado(SoftDeleteModel):
    voluntario = models.ForeignKey("persona.Voluntario", on_delete=models.CASCADE, related_name="certificados")
    voluntariado = models.ForeignKey("voluntariado.Voluntariado", null=True, blank=True, on_delete=models.SET_NULL)
    horas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fecha_emision = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Certificado {self.voluntario} - {self.horas}h"
