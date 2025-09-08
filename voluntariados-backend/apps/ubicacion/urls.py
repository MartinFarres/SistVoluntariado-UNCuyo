from rest_framework import routers
from django.urls import path, include
from .views import PaisViewSet, ProvinciaViewSet, DepartamentoViewSet, LocalidadViewSet

router = routers.DefaultRouter()
router.register(r'paises', PaisViewSet, basename='pais')
router.register(r'provincias', ProvinciaViewSet, basename='provincia')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'localidades', LocalidadViewSet, basename='localidad')

urlpatterns = [path('', include(router.urls))]
