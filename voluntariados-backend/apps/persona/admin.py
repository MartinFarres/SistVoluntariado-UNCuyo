from django.contrib import admin
from .models import Persona, Voluntario, Gestionador, Administrativo, Delegado

class PersonaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "dni", "is_active")
    search_fields = ("nombre", "apellido", "dni")

class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "dni", "carrera", "interno", "condicion", "is_active")
    search_fields = ("nombre", "apellido", "dni")
    list_filter = ("condicion",)

admin.site.register(Persona, PersonaAdmin)
admin.site.register(Voluntario, VoluntarioAdmin)
admin.site.register(Gestionador)
admin.site.register(Administrativo)
admin.site.register(Delegado)
