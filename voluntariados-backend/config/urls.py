# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.users.urls')),
    path('api/persona/', include('apps.personas.urls')),
    path('api/', include('apps.voluntariados.urls')),
    path('api/', include('apps.voluntarios.urls')),
    path('api/ubicacion/', include('apps.ubicacion.urls')),
    path('api/', include('apps.organizacion.urls')),
    path('api/', include('apps.facultad.urls')),
    path('api/', include('apps.capacitacion.urls')),
    path('api/', include('apps.asistencia.urls')),
    path('api/', include('apps.certificado.urls')),
]
