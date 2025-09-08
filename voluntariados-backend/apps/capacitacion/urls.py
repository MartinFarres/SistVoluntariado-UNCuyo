from rest_framework import routers
from django.urls import path, include
from .views import CapacitacionViewSet, InscripcionCapacitacionViewSet

router = routers.DefaultRouter()
router.register(r'capacitaciones', CapacitacionViewSet, basename='capacitacion')
router.register(r'inscripciones-capacitacion', InscripcionCapacitacionViewSet, basename='inscripcion-capacitacion')

urlpatterns = [path('', include(router.urls))]
