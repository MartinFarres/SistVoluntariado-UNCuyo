from rest_framework import routers
from django.urls import path, include
from .views import CertificadoViewSet, AutoridadViewSet

router = routers.DefaultRouter()
router.register(r'certificado', CertificadoViewSet, basename='certificado')
router.register(r'autoridad', AutoridadViewSet, basename='autoridad')
urlpatterns = [path('', include(router.urls))]
