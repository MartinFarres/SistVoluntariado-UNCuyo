from rest_framework import viewsets, permissions
from .models import Organizacion
from .serializers import OrganizacionSerializer

class OrganizacionViewSet(viewsets.ModelViewSet):
    """
    CRUD de Organizaciones.
    Lectura: pública/autenticada según settings.
    Escritura: solo usuarios autenticados (o restringir a admin/delegado).
    """
    queryset = Organizacion.objects.select_related("contacto_persona", "localidad").all()
    serializer_class = OrganizacionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    