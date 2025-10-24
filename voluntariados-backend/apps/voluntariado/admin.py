from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import DescripcionVoluntariado, Voluntariado, Turno, InscripcionTurno


@admin.register(Voluntariado)
class VoluntariadoAdmin(SimpleHistoryAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(DescripcionVoluntariado)
class DescripcionVoluntariadoAdmin(SimpleHistoryAdmin):
    search_fields = ('resumen',)


@admin.register(Turno)
class TurnoAdmin(SimpleHistoryAdmin):
    list_display = ('voluntariado', 'fecha', 'hora_inicio', 'hora_fin', 'cupo')
    list_filter = ('voluntariado__nombre',)
    search_fields = ('lugar',)


@admin.register(InscripcionTurno)
class InscripcionTurnoAdmin(SimpleHistoryAdmin):
    list_display = ('turno', 'voluntario', 'estado', 'fecha_inscripcion')
    list_filter = ('estado', 'turno__voluntariado__nombre')
    search_fields = ('voluntario__persona__nombre', 'voluntario__persona__apellido')
