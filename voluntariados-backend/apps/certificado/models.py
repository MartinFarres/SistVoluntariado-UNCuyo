from django.db import models

class Certificado(models.Model):
    voluntario = models.ForeignKey("persona.Voluntario", on_delete=models.CASCADE, related_name="certificados")
    voluntariado = models.ForeignKey("voluntariado.Voluntariado", null=True, blank=True, on_delete=models.SET_NULL)
    horas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    # Chequear si usar FileField o URLField (si se guardan en S3 u otro servicio)
    archivo = models.FileField(upload_to="certificados/", null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True)
    creado_por = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Certificado {self.voluntario} - {self.horas}h"
