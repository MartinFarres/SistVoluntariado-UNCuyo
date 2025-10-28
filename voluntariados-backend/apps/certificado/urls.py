from rest_framework import routers
from django.urls import path, include
from .views import (
    CertificadoGeneracionViewSet,
    upload_template,
    generar_desde_admin,
)

router = routers.DefaultRouter()
# Endpoint para generación de certificados (voluntario autenticado)
router.register(r'generacion', CertificadoGeneracionViewSet, basename='certificado-generacion')

urlpatterns = [
    path('', include(router.urls)),

    # 📤 Subir / reemplazar plantilla
    path('plantilla/', upload_template, name='upload-template'),

    # 🧾 Generar certificado desde admin
    path('generar-desde-admin/', generar_desde_admin, name='generar-desde-admin'),
]