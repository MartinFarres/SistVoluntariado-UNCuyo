from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/personas/', include('apps.personas.urls')),
    path('api/voluntariados/', include('apps.voluntariados.urls')),
    path('api/asistencia/', include('apps.asistencia.urls')),
    # ...add more as needed...
]