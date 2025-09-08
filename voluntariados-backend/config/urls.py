# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),

    # Apps principales (cada una debe tener apps/<app>/urls.py)
    path('api/users/', include('apps.users.urls')),
    path('api/personas/', include('apps.personas.urls')),
    path('api/voluntariados/', include('apps.voluntariados.urls')),
    path('api/turnos/', include('apps.voluntariados.urls')),         
    path('api/inscripciones/', include('apps.voluntariados.urls')),  

    path('api/voluntarios/', include('apps.voluntarios.urls')),
    path('api/ubicacion/', include('apps.ubicacion.urls')),
    path('api/organizaciones/', include('apps.organizacion.urls')),
    path('api/facultades/', include('apps.facultad.urls')),
    path('api/capacitaciones/', include('apps.capacitacion.urls')),
    path('api/asistencias/', include('apps.asistencia.urls')),
    path('api/certificado/', include('apps.certificado.urls')),

]
