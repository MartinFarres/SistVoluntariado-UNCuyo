from django.db import models

class Capacitacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    cupo = models.PositiveIntegerField(null=True, blank=True)
    voluntariado = models.ForeignKey("voluntariados.Voluntariado", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.titulo

class InscripcionCapacitacion(models.Model):
    capacitacion = models.ForeignKey(Capacitacion, on_delete=models.CASCADE, related_name="inscripciones")
    voluntario = models.ForeignKey("voluntarios.Voluntario", on_delete=models.CASCADE, related_name="cap_inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        unique_together = ("capacitacion", "voluntario")
