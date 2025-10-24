from rest_framework import routers
from django.urls import path, include
from .views import VoluntariadoViewSet, TurnoViewSet, InscripcionTurnoViewSet, DescripcionVoluntariadoViewSet, InscripcionConvocatoriaViewSet

router = routers.DefaultRouter()
router.register(r'voluntariados', VoluntariadoViewSet, basename='voluntariados')
router.register(r'descripcion', DescripcionVoluntariadoViewSet, basename='descripcion')
router.register(r'turnos', TurnoViewSet, basename='turno')
router.register(r'inscripciones', InscripcionTurnoViewSet, basename='inscripcion-turno')
router.register(r'inscripciones-convocatoria', InscripcionConvocatoriaViewSet, basename='inscripcion-convocatoria')

urlpatterns = [path('', include(router.urls))]
