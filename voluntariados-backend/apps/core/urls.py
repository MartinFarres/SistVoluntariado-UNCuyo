from django.urls import path
from .views import (
    LandingConfigRetrieveView,
    LandingConfigUpdateView,
    landing_config_public,
    landing_config_admin
)

app_name = 'core'

urlpatterns = [
    # Endpoint público para obtener configuración básica
    path('landing-config/public/', landing_config_public, name='landing-config-public'),
    
    # Endpoints para administradores
    path('landing-config/admin/', landing_config_admin, name='landing-config-admin'),
    
    # Endpoints con vistas basadas en clases (alternativas)
    path('landing-config/', LandingConfigRetrieveView.as_view(), name='landing-config-retrieve'),
    path('landing-config/update/', LandingConfigUpdateView.as_view(), name='landing-config-update'),
]