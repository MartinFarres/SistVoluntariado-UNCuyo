from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

from apps.persona.models import Gestionador
from apps.soft_delete.model import SoftDeleteModel


class DescripcionVoluntariado(SoftDeleteModel):
    descripcion = models.TextField(blank=True)
    logo = models.FileField(upload_to="logos", null=True, blank=True)
    portada = models.FileField(upload_to="logos", null=True, blank=True)
    resumen = models.TextField(blank=True)
    history = HistoricalRecords()


# Custom HistoricalRecords manager to adjust db_column for the historical model
class VoluntariadoHistoricalRecords(HistoricalRecords):
    def get_historical_model(self, model):
        historical_model = super().get_historical_model(model)
        # Find the 'gestionadores' field in the historical model and set its db_column
        # This assumes the field exists and is a ForeignKey
        if hasattr(historical_model, 'gestionadores'):
            field = historical_model._meta.get_field('gestionadores')
            if isinstance(field, models.ForeignKey):
                field.db_column = 'gestionadores_id' # Force lowercase db_column for the historical table
        return historical_model


class Voluntariado(SoftDeleteModel):
    nombre = models.CharField(max_length=250)
    descripcion = models.ForeignKey(DescripcionVoluntariado, on_delete=models.SET_NULL, related_name='voluntariados',null=True)
    gestionadores = models.ForeignKey(Gestionador, on_delete=models.SET_NULL, related_name='voluntariados',null=True, db_column='gestionadores_id')
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

    history = VoluntariadoHistoricalRecords() # Use our custom manager

    def __str__(self):
        return self.nombre


class Turno(SoftDeleteModel):
    voluntariado = models.ForeignKey("Voluntariado", on_delete=models.CASCADE,null=True, related_name="turnos")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cupo = models.PositiveIntegerField(default=1)
    lugar = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ("-fecha", "hora_inicio")

    def __str__(self):
        return f"{self.fecha}: {self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"


class InscripcionTurno(SoftDeleteModel):
    class Status(models.TextChoices):
        INSCRITO = "INS", "Inscrito"
        CANCELADO = "CAN", "Cancelado"
        ASISTIO = "ASI", "Asistió"

    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, related_name="inscripciones")
    voluntario = models.ForeignKey("persona.Voluntario", on_delete=models.CASCADE, related_name="inscripciones")
    estado = models.CharField(max_length=4, choices=Status.choices, default=Status.INSCRITO)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
