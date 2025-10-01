# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # JWT Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("api-auth/", include("rest_framework.urls")),  # login/logout web
    path('admin/', admin.site.urls),
    
    # Include router URLs
    path('api/', include(router.urls)),
    
    path('api/persona/', include('apps.persona.urls')),
    path('api/voluntariado/', include('apps.voluntariado.urls')),
    path('api/ubicacion/', include('apps.ubicacion.urls')),
    path('api/organizacion/', include('apps.organizacion.urls')),
    path('api/facultad/', include('apps.facultad.urls')),
    path('api/capacitacion/', include('apps.capacitacion.urls')),
    path('api/asistencia/', include('apps.asistencia.urls')),
    path('api/certificado/', include('apps.certificado.urls')),
]