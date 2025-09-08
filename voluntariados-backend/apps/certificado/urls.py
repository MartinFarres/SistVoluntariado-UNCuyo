from rest_framework import routers
from django.urls import path, include
from .views import CertificadoViewSet

router = routers.DefaultRouter()
router.register(r'certificado', CertificadoViewSet, basename='certificado')

urlpatterns = [path('', include(router.urls))]
