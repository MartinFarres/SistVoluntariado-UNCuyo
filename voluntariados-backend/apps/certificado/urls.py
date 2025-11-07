from django.urls import path
from .views import (
    upload_template,
    generar_desde_admin,
    generar_por_valores_admin,
    generar_por_voluntariado,
    horas_por_voluntariado,
)

urlpatterns = [
    # Generación para voluntario autenticado (sin listado)
    path('generacion/generar-por-voluntariado/<int:voluntariado_id>/', generar_por_voluntariado, name='generar-por-voluntariado'),

    # Endpoint to get total horas for the authenticated user and a given voluntariado
    path('generacion/horas-por-voluntariado/<int:voluntariado_id>/', horas_por_voluntariado, name='horas-por-voluntariado'),

    # Subir / reemplazar plantilla
    path('plantilla/', upload_template, name='upload-template'),

    # Generar certificado desde admin
    path('generar-desde-admin/', generar_desde_admin, name='generar-desde-admin'),
    # Test: generar certificado desde valores (admin only). Accepts JSON.
    path('generar-por-valores/', generar_por_valores_admin, name='generar-por-valores-admin'),
]