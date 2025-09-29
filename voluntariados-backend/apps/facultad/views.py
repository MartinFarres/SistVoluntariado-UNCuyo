from rest_framework import viewsets, permissions
from .models import Facultad, Carrera
from .serializers import FacultadSerializer, CarreraSerializer
from apps.users.permissions import IsAdministrador

class FacultadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Facultades.
    Solo los administradores tienen permiso para acceder a estas vistas.
    """
    queryset = Facultad.objects.all().order_by('nombre')
    serializer_class = FacultadSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]

class CarreraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Carreras.
    Solo los administradores tienen permiso para acceder a estas vistas.
    """
    queryset = Carrera.objects.all().order_by('nombre')
    serializer_class = CarreraSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
