from rest_framework import viewsets, permissions
from .models import Facultad, Carrera
from .serializers import FacultadSerializer, CarreraSerializer

class FacultadViewSet(viewsets.ModelViewSet):
    """
    CRUD de Facultades. Lectura pública, escritura autenticada (cambiar si hace falta).
    """
    queryset = Facultad.objects.prefetch_related("carreras").all()
    serializer_class = FacultadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CarreraViewSet(viewsets.ModelViewSet):
    """
    CRUD de Carreras. Al crear una carrera pasás `facultad` (PK) en el payload.
    """
    queryset = Carrera.objects.select_related("facultad").all()
    serializer_class = CarreraSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
