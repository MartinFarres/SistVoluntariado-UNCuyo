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

    requiere_convocatoria = models.BooleanField(default=True, verbose_name="Requiere convocatoria")

    organizacion = models.ForeignKey(
        "organizacion.Organizacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Fechas de convocatoria
    fecha_inicio_convocatoria = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio de convocatoria")
    fecha_fin_convocatoria = models.DateField(null=True, blank=True, verbose_name="Fecha de fin de convocatoria")
    
    # Fechas de cursado del voluntariado
    fecha_inicio_cursado = models.DateField(null=False, blank=True, verbose_name="Fecha de inicio de cursado")
    fecha_fin_cursado = models.DateField(null=False, blank=True, verbose_name="Fecha de fin de cursado")

    history = VoluntariadoHistoricalRecords() # Use our custom manager

    # Ubicación geográfica
    latitud = models.FloatField(null=False, blank=True, verbose_name="Latitud")
    longitud = models.FloatField(null=False, blank=True, verbose_name="Longitud")
    place_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID de lugar (Google Maps)")

    def save(self, *args, **kwargs):
        """
        Override save to clean up turnos when cursado dates change.
        If fecha_inicio_cursado or fecha_fin_cursado are modified,
        delete all turnos that fall outside the new date range.
        """
        # Check if this is an update (not a new instance)
        if self.pk:
            try:
                # Get the old instance from database
                old_instance = Voluntariado.objects.get(pk=self.pk)
                
                # Check if cursado dates have changed
                dates_changed = (
                    old_instance.fecha_inicio_cursado != self.fecha_inicio_cursado or
                    old_instance.fecha_fin_cursado != self.fecha_fin_cursado
                )
                
                if dates_changed and self.fecha_inicio_cursado and self.fecha_fin_cursado:
                    # Save first to update the model
                    super().save(*args, **kwargs)
                    
                    # Delete turnos outside the new date range
                    turnos_to_delete = self.turnos.filter(
                        models.Q(fecha__lt=self.fecha_inicio_cursado) |
                        models.Q(fecha__gt=self.fecha_fin_cursado)
                    )
                    
                    if turnos_to_delete.exists():
                        turnos_to_delete.delete()
                    
                    return  # Exit early since we already saved
            except Voluntariado.DoesNotExist:
                # Old instance doesn't exist (shouldn't happen, but handle gracefully)
                pass
        
        # Normal save for new instances or when dates haven't changed
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """
        Cascade soft delete to related objects:
        - All Turnos (which will cascade to InscripcionTurno)
        - All InscripcionConvocatoria
        """
        # Soft delete all related turnos (each Turno will handle its own cascades)
        self.turnos.all().delete()
        
        # Soft delete all related inscripciones de convocatoria
        self.inscripciones.all().delete()
        
        # Finally, soft delete the Voluntariado itself
        super().delete(using=using, keep_parents=keep_parents)

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

    def delete(self, using=None, keep_parents=False):
        """
        Cascade soft delete to related InscripcionTurno
        (which will cascade to Asistencias)
        """
        # Soft delete all related inscripciones (each will handle its own cascades)
        self.inscripciones.all().delete()
        
        # Finally, soft delete the Turno itself
        super().delete(using=using, keep_parents=keep_parents)

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

    def delete(self, using=None, keep_parents=False):
        """
        Cascade soft delete to related Asistencia (if exists)
        """
        # Soft delete the asistencia if it exists (OneToOne relation)
        if hasattr(self, 'asistencia'):
            self.asistencia.delete()
        
        # Finally, soft delete the InscripcionTurno itself
        super().delete(using=using, keep_parents=keep_parents)


class InscripcionConvocatoria(SoftDeleteModel):
    class Status(models.TextChoices):
        INSCRITO = "INS", "Inscrito" # Inscripción activa
        CANCELADO = "CAN", "Cancelado" # Inscripción cancelada
        ACEPTADO = "ACE", "Aceptado" # Inscripción aceptada por un gestionador
        RECHAZADO = "REJ", "Rechazado" # Inscripción rechazada por un gestionador

    voluntariado = models.ForeignKey(Voluntariado, on_delete=models.CASCADE, related_name="inscripciones")
    voluntario = models.ForeignKey("persona.Voluntario", on_delete=models.CASCADE, related_name="inscripciones_convocatorias")
    estado = models.CharField(max_length=4, choices=Status.choices, default=Status.INSCRITO)