from rest_framework import viewsets, permissions
from .models import Pais, Provincia, Departamento, Localidad
from .serializers import PaisSerializer, ProvinciaSerializer, DepartamentoSerializer, LocalidadSerializer

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.select_related("pais").all()
    serializer_class = ProvinciaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.select_related("provincia").all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LocalidadViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.select_related("departamento__provincia").all()
    serializer_class = LocalidadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
