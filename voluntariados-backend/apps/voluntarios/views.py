from rest_framework import viewsets, permissions
from .models import Voluntario
from .serializers import VoluntarioSerializer

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permite edición sólo a staff (administrativo) o usuarios autenticados con permisos especiales.
    Lectura pública (si querés restringir lectura, cambiá).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.role == "ADMIN")

class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.select_related("persona", "carrera").all()
    serializer_class = VoluntarioSerializer
    permission_classes = [IsStaffOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Aquí podrías agregar lógica para filtrar por parámetros de consulta
        dni = self.request.query_params.get('dni', None)
        if dni is not None:
            queryset = queryset.filter(persona__dni=dni)
        # Agrega más filtros según sea necesario    
        return queryset
    
    