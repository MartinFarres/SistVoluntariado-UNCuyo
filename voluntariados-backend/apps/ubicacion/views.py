from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from .models import Pais, Provincia, Departamento, Localidad
from .serializers import PaisSerializer, ProvinciaSerializer, DepartamentoSerializer, LocalidadSerializer
from apps.users.permissions import IsAdministrador
class PaisViewSet(viewsets.ModelViewSet):
    """ViewSet para Pais: lista/creación pública en GET; admin para crear/editar/eliminar."""
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

    def get_permissions(self):
        # Allow public GET, but only admin can create/update/delete
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdministrador()]


class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdministrador()]


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdministrador()]


class LocalidadViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdministrador()]