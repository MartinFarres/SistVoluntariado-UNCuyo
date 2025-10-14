from rest_framework import viewsets, permissions
from .models import Facultad, Carrera
from .serializers import FacultadSerializer, CarreraSerializer
from apps.users.permissions import IsAdministrador

class FacultadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Facultades.
    Cualquiera puede ver las facultades, pero solo los administradores pueden crear, actualizar o eliminar.
    """
    queryset = Facultad.objects.all().order_by('nombre')
    serializer_class = FacultadSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdministrador()]

class CarreraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Carreras.
    Cualquiera puede ver las carreras, pero solo los administradores pueden crear, actualizar o eliminar.
    """
    queryset = Carrera.objects.all().order_by('nombre')
    serializer_class = CarreraSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdministrador()]
