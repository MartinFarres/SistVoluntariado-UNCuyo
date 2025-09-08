from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Asistencia
from .serializers import AsistenciaSerializer

class IsAdminOrDelegado(permissions.BasePermission):
    """
    Permite crear/editar asistencias solo a usuarios con role ADMIN o DELEG.
    Lectura: usuarios autenticados (o más restrictivo si querés).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # métodos no seguros -> sólo admin o delegado
        return request.user and request.user.is_authenticated and request.user.role in ("ADMIN", "DELEG")

    def has_object_permission(self, request, view, obj):
        # mismas reglas para object-level por defecto
        return self.has_permission(request, view)

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.select_related("inscripcion__turno", "inscripcion__voluntario__persona").all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAdminOrDelegado]

    def perform_create(self, serializer):
        # asignamos quien registró la asistencia
        serializer.save(registrada_por=self.request.user)

    def perform_update(self, serializer):
        serializer.save(registrada_por=self.request.user)
