from rest_framework import routers
from django.urls import path, include
from .views import AsistenciaViewSet

router = routers.DefaultRouter()
router.register(r'asistencias', AsistenciaViewSet, basename='asistencia')

urlpatterns = [path('', include(router.urls))]
