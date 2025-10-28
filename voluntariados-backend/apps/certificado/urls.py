from rest_framework import routers
from django.urls import path, include
from .views import CertificadoViewSet, AutoridadViewSet, EncabezadoCertificadoViewSet

router = routers.DefaultRouter()
router.register(r'certificados', CertificadoViewSet, basename='certificado')
router.register(r'autoridades', AutoridadViewSet, basename='autoridad')
router.register(r'encabezados', EncabezadoCertificadoViewSet, basename='encabezado')  # 👈 NUEVA RUTA

urlpatterns = [
    path('', include(router.urls)),
]
