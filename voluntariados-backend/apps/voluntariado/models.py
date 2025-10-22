from django.db import models
from django.conf import settings

from apps.persona.models import Gestionador
from apps.soft_delete.model import SoftDeleteModel


class DescripcionVoluntariado(SoftDeleteModel):
    descripcion = models.TextField(blank=True)
    logo = models.FileField(upload_to="logos", null=True, blank=True)
    portada = models.FileField(upload_to="logos", null=True, blank=True)
    resumen = models.TextField(blank=True)


class Voluntariado(SoftDeleteModel):
    nombre = models.CharField(max_length=250)
    descripcion = models.ForeignKey(DescripcionVoluntariado, on_delete=models.SET_NULL, related_name='voluntariados',null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    gestionadores = models.ForeignKey(Gestionador, on_delete=models.SET_NULL, related_name='voluntariados',null=True)
    organizacion = models.ForeignKey(
        "organizacion.Organizacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    estado_choices = [
        ("DRAFT", "Borrador"),
        ("ACTIVE", "Activo"),
        ("CLOSED", "Cerrado"),
    ]
    estado = models.CharField(max_length=10, choices=estado_choices, default="DRAFT")

    def __str__(self):
        return self.nombre

class Turno(SoftDeleteModel):
    voluntariado = models.ForeignKey("Voluntariado", on_delete=models.CASCADE,null=True, related_name="turnos")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cupo = models.PositiveIntegerField(default=1)
    lugar = models.CharField(max_length=255, null=True, blank=True) # checkaer si usar ForeignKey a "Ubicación"

    class Meta:
        ordering = ("-fecha", "hora_inicio")   # orden por defecto: más recientes primero

    def __str__(self):
        return f"{self.fecha}: {self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"


class InscripcionTurno(SoftDeleteModel):
    class Status(models.TextChoices): # (?? agregar estado de en espera de aprobación)
        INSCRITO = "INS", "Inscrito"
        CANCELADO = "CAN", "Cancelado"
        ASISTIO = "ASI", "Asistió"

    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, related_name="inscripciones")
    voluntario = models.ForeignKey("persona.Voluntario", on_delete=models.CASCADE, related_name="inscripciones")
    estado = models.CharField(max_length=4, choices=Status.choices, default=Status.INSCRITO)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

#    class Meta:
#        unique_together = ("turno", "voluntario")

#    def __str__(self):
#       return f"{self.voluntario} -> {self.turno} ({self.get_estado_display()})"
