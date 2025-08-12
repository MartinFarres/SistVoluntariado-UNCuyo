from django.db import models
from django.conf import settings

class Voluntariado(models.Model):
    titulo = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True)
    organizacion = models.ForeignKey("organizacion.Organizacion", on_delete=models.PROTECT, related_name="voluntariados")
    facultad = models.ForeignKey("facultad.Facultad", null=True, blank=True, on_delete=models.SET_NULL)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado_choices = [
        ("DRAFT", "Borrador"),
        ("ACTIVE", "Activo"),
        ("CLOSED", "Cerrado"),
    ]
    estado = models.CharField(max_length=10, choices=estado_choices, default="DRAFT")
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Turno(models.Model):
    voluntariado = models.ForeignKey(Voluntariado, on_delete=models.CASCADE, related_name="turnos")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cupo = models.PositiveIntegerField(default=1)
    lugar = models.CharField(max_length=255, null=True, blank=True) # checkaer si usar ForeignKey a "Ubicación"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-fecha", "hora_inicio")   # orden por defecto: más recientes primero

    def __str__(self):
        return f"{self.voluntariado.titulo} - {self.fecha} {self.hora_inicio}"

class InscripcionTurno(models.Model):
    class Status(models.TextChoices): # (?? agregar estado de en espera de aprobación)
        INSCRITO = "INS", "Inscripto"
        CANCELADO = "CAN", "Cancelado"
        ASISTIO = "ASI", "Asistió"

    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, related_name="inscripciones")
    voluntario = models.ForeignKey("voluntarios.Voluntario", on_delete=models.CASCADE, related_name="inscripciones")
    estado = models.CharField(max_length=4, choices=Status.choices, default=Status.INSCRITO)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("turno", "voluntario")

    def __str__(self):
        return f"{self.voluntario} -> {self.turno} ({self.get_estado_display()})"
