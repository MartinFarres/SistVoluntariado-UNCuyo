# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/users/', include('apps.users.urls')),
    path('api/persona/', include('apps.persona.urls')),
    path('api/voluntariado/', include('apps.voluntariado.urls')),
    path('api/ubicacion/', include('apps.ubicacion.urls')),
    path('api/organizacion/', include('apps.organizacion.urls')),
    path('api/facultad/', include('apps.facultad.urls')),
    path('api/capacitacion/', include('apps.capacitacion.urls')),
    path('api/asistencia/', include('apps.asistencia.urls')),
    path('api/certificado/', include('apps.certificado.urls')),
]
