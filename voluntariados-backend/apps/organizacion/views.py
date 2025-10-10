from rest_framework import viewsets, permissions
from .models import Organizacion
from .serializers import OrganizacionSerializer
from apps.users.permissions import IsAdministrador

class OrganizacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Organizaciones.

    Permite operaciones CRUD completas (Crear, Leer, Actualizar, Borrar).
    Solo los administradores tienen permiso para acceder a estas vistas.
    """
    queryset = Organizacion.objects.all().order_by('nombre')
    serializer_class = OrganizacionSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "list"):
            return [permissions.IsAuthenticatedOrReadOnly()]
        else:
            return [permissions.IsAuthenticated(), IsAdministrador()]
    
