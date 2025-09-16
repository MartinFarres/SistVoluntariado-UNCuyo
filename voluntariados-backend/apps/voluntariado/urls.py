from rest_framework import routers
from django.urls import path, include
from .views import VoluntariadoViewSet, TurnoViewSet, InscripcionTurnoViewSet

router = routers.DefaultRouter()
router.register(r'voluntariados', VoluntariadoViewSet, basename='voluntariados')
router.register(r'turnos', TurnoViewSet, basename='turno')
router.register(r'inscripciones', InscripcionTurnoViewSet, basename='inscripcion-turno')

urlpatterns = [path('', include(router.urls))]
