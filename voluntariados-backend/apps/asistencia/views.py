from rest_framework import viewsets
from .models import Asistencia
from .serializers import AsistenciaSerializer
from apps.users.permissions import IsGestionador

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.select_related('inscripcion__turno', 'inscripcion__voluntario').all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsGestionador]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show asistencia for active inscriptions (not cancelled)
        queryset = queryset.filter(inscripcion__is_active=True)
        
        turno_id = self.request.query_params.get('turno', None)
        if turno_id is not None:
            queryset = queryset.filter(inscripcion__turno__id=turno_id)
        return queryset