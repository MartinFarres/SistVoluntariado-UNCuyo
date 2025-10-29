from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Persona, Voluntario, Administrativo, Delegado, Gestionador
from .serializers import PersonaSerializer, VoluntarioSerializer, AdministrativoSerializer, DelegadoSerializer, GestionadorSerializer
from apps.users.permissions import IsAdministrador, IsGestionador
from apps.voluntariado.models import InscripcionTurno, Voluntariado
from apps.voluntariado.serializers import VoluntariadoConTurnosSerializer
from apps.asistencia.models import Asistencia
from django.db.models import Sum


class IsAdminOrSelfOwner(permissions.BasePermission):
    """
    Permite el acceso solo a administradores o al propietario del objeto.
    El propietario se determina si request.user.persona.pk coincide con el pk del objeto.
    """
    def has_permission(self, request, view):
        # Los administradores siempre tienen permiso
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        # Permitir list y create a administradores (ya cubierto por has_object_permission para retrieve, update, destroy)
        if view.action in ['list', 'create']:
            return request.user and request.user.is_authenticated and request.user.is_staff
        # Para otras acciones (retrieve, update, destroy), se verifica a nivel de objeto
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Los administradores siempre tienen permiso
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True

        # Si el usuario tiene una persona asociada, verificar si es el propietario del objeto
        if hasattr(request.user, 'persona') and request.user.persona.pk == obj.pk:
            return True
        
        # Para Voluntario, Administrativo, Delegado, también verificar si la persona asociada es el propietario
        if isinstance(obj, (Voluntario, Administrativo, Delegado)) and hasattr(request.user, 'persona') and request.user.persona.pk == obj.persona.pk:
            return True

        return False


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        # Para retrieve, update, partial_update, destroy, se requiere ser admin o el propio usuario
        return [IsAdminOrSelfOwner()]


class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        
        if self.action == 'observaciones_asistencia':
            return [IsGestionador()]
        
        # Para voluntariados, horas, retrieve, update, partial_update, destroy
        # se requiere ser admin o el propio voluntario
        return [IsAdminOrSelfOwner()]

    def get_queryset(self):
        queryset = super().get_queryset()
        condicion = self.request.query_params.get('condicion')
        if condicion:
            queryset = queryset.filter(condicion=condicion)
        return queryset

    @action(detail=False, methods=['get'], url_path='count', permission_classes=[IsAdministrador])
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
            # La verificación de permisos se realiza en IsAdminOrSelfOwner

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

    @action(detail=True, methods=['get'], url_path='observaciones-asistencia')
    def observaciones_asistencia(self, request, pk=None):
        """Devuelve las observaciones de asistencia para un voluntario específico."""
        try:
            voluntario = self.get_object()
            observaciones = Asistencia.objects.filter(
                inscripcion__voluntario=voluntario
            ).exclude(observaciones__isnull=True).exclude(observaciones__exact='').values_list('observaciones', flat=True)
            return Response(list(observaciones))
        except Voluntario.DoesNotExist:
            return Response({"detail": "Voluntario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "Ocurrió un error al procesar la solicitud."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='horas')
    def horas(self, request, pk=None):
        """
        Devuelve la suma de horas registradas en Asistencia para un voluntario específico.
        Endpoint: GET /persona/voluntarios/{id}/horas/
        Response: { "total_horas": 12.5 }
        """
        try:
            voluntario = self.get_object()
            # La verificación de permisos se realiza en IsAdminOrSelfOwner

            total = Asistencia.objects.filter(
                inscripcion__voluntario=voluntario,
                is_active=True,
            ).aggregate(total_horas=Sum('horas'))

            total_horas = total.get('total_horas') or 0
            # Convert Decimal to float for JSON serialization
            try:
                total_horas_val = float(total_horas)
            except Exception:
                total_horas_val = 0

            return Response({"total_horas": total_horas_val}, status=status.HTTP_200_OK)

        except Voluntario.DoesNotExist:
            return Response({"detail": "Voluntario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
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
        return [IsAdminOrSelfOwner()]

class DelegadoViewSet(viewsets.ModelViewSet):
    queryset = Delegado.objects.all()
    serializer_class = DelegadoSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdministrador()]
        return [IsAdminOrSelfOwner()]
