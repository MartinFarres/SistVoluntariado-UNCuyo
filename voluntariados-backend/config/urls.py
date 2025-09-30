# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from apps.users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("accounts/", include("allauth.urls")),  # django-allauth endpoints
    path("auth/", include("dj_rest_auth.urls")),  # login/logout con token
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/social/", include("allauth.socialaccount.urls")),  # social login

    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('admin/', admin.site.urls),
    
    path('api/persona/', include('apps.persona.urls')),
    path('api/voluntariado/', include('apps.voluntariado.urls')),
    path('api/ubicacion/', include('apps.ubicacion.urls')),
    path('api/organizacion/', include('apps.organizacion.urls')),
    path('api/facultad/', include('apps.facultad.urls')),
    path('api/capacitacion/', include('apps.capacitacion.urls')),
    path('api/asistencia/', include('apps.asistencia.urls')),
    path('api/certificado/', include('apps.certificado.urls')),
]
