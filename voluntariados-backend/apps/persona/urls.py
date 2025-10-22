from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PersonaViewSet,
    VoluntarioViewSet,
    AdministrativoViewSet,
    DelegadoViewSet,
    GestionadorViewSet
)

router = DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona')
router.register(r'voluntarios', VoluntarioViewSet, basename='voluntario')
router.register(r'administrativos', AdministrativoViewSet, basename='administrativo')
router.register(r'delegados', DelegadoViewSet, basename='delegado')
router.register(r'gestionadores', GestionadorViewSet, basename='gestionador')


urlpatterns = [
    path('', include(router.urls)),
]

