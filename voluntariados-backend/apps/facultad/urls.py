from rest_framework import routers
from django.urls import path, include
from .views import FacultadViewSet, CarreraViewSet

router = routers.DefaultRouter()
router.register(r'facultades', FacultadViewSet, basename='facultad')
router.register(r'carreras', CarreraViewSet, basename='carrera')

urlpatterns = [path('', include(router.urls))]
