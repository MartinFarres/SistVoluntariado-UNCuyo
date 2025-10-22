from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Persona, Voluntario, Administrativo, Delegado, Gestionador
from .serializers import PersonaSerializer, VoluntarioSerializer, AdministrativoSerializer, DelegadoSerializer, GestionadorSerializer
from apps.users.permissions import IsAdministrador, CanUpdateOwnPersona
from apps.voluntariado.models import InscripcionTurno, Voluntariado
from apps.voluntariado.serializers import VoluntariadoConTurnosSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        return [CanUpdateOwnPersona()]

class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        if self.action in ['voluntariados', 'count']:
            return [permissions.IsAuthenticated()]
        return [CanUpdateOwnPersona()]

    @action(detail=False, methods=['get'], url_path='count', permission_classes=[permissions.IsAuthenticated])
    def count(self, request):
        """
        Returns total number of voluntarios.
        Lightweight endpoint for dashboards to avoid fetching full lists.
        """
        try:
            total = Voluntario.objects.count()
            return Response({"count": total})
        except Exception:
            return Response({"detail": "Error al obtener el total de voluntarios."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def voluntariados(self, request, pk=None):
        try:
            voluntario = self.get_object()
            
            if not (request.user.is_staff or (hasattr(request.user, 'persona') and request.user.persona.pk == voluntario.pk)):
                 return Response({"detail": "No tiene permiso para ver estos voluntariados."}, status=status.HTTP_403_FORBIDDEN)

            inscripciones = InscripcionTurno.objects.filter(voluntario=voluntario).select_related(
                'turno__voluntariado', 
                'turno__voluntariado__organizacion', 
                'turno__voluntariado__descripcion'
            )
            
            voluntariados_ids = inscripciones.values_list('turno__voluntariado_id', flat=True).distinct()
            voluntariados = Voluntariado.objects.filter(id__in=voluntariados_ids)

            serializer = VoluntariadoConTurnosSerializer(voluntariados, many=True, context={'request': request, 'voluntario_id': voluntario.id})

            return Response(serializer.data)

        except Voluntario.DoesNotExist:
            return Response({"detail": "Voluntario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # You might want to log the error `e` here
            return Response({"detail": "Ocurrió un error al procesar la solicitud."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GestionadorViewSet(viewsets.ModelViewSet):
    queryset = Gestionador.objects.all()
    serializer_class = GestionadorSerializer
    permission_classes = [IsAdministrador]

class AdministrativoViewSet(viewsets.ModelViewSet):
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        return [CanUpdateOwnPersona()]

class DelegadoViewSet(viewsets.ModelViewSet):
    queryset = Delegado.objects.all()
    serializer_class = DelegadoSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        return [CanUpdateOwnPersona()]

