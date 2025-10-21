from rest_framework import viewsets
from .models import Asistencia
from .serializers import AsistenciaSerializer
from apps.users.permissions import IsGestionador

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.select_related('inscripcion__turno', 'inscripcion__voluntario').all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsGestionador]