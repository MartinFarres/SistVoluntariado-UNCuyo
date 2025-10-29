from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Capacitacion, InscripcionCapacitacion
from .serializers import CapacitacionSerializer, InscripcionCapacitacionSerializer
from apps.persona.models import Voluntario
from apps.users.permissions import IsGestionador

class CapacitacionViewSet(viewsets.ModelViewSet):
    """
    CRUD de capacitaciones.
    - GET /capacitaciones/         -> list (público)
    - POST /capacitaciones/        -> create (solo gestores)
    - GET /capacitaciones/{pk}/    -> retrieve (público)
    - PUT/PATCH /capacitaciones/{pk}/ -> update (solo gestores)
    - DELETE /capacitaciones/{pk}/ -> destroy (solo gestores)
    - POST /capacitaciones/{pk}/inscribirse/ -> acción custom para inscribirse (solo voluntarios autenticados)
    """
    queryset = Capacitacion.objects.select_related("voluntariado").all()
    serializer_class = CapacitacionSerializer

    def get_permissions(self):
        """
        Instancia y devuelve la lista de permisos que requiere esta vista.
        - IsGestionador para acciones de escritura (create, update, partial_update, destroy).
        - IsAuthenticated para inscribirse.
        - AllowAny para el resto (list, retrieve).
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsGestionador]
        elif self.action == 'inscribirse':
            permission_classes = [permissions.IsAuthenticated]
        else: # 'list', 'retrieve'
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def inscribirse(self, request, pk=None):
        """
        Inscribe al voluntario del usuario autenticado en la capacitación.
        Devuelve 201 con la inscripción o 400 con motivo.
        """
        cap = get_object_or_404(Capacitacion, pk=pk)

        persona = getattr(request.user, "persona", None)
        if not persona:
            return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            voluntario = persona.voluntario
        except Voluntario.DoesNotExist:
            return Response({"detail": "La persona no está registrada como voluntario."}, status=status.HTTP_400_BAD_REQUEST)

        # bloqueo/chequeo de cupo y duplicados dentro de transacción
        with transaction.atomic():
            # recargar con lock si esperás concurrencia alta:
            cap_locked = Capacitacion.objects.select_for_update().filter(pk=cap.pk).first()

            # duplicado
            if InscripcionCapacitacion.objects.filter(capacitacion=cap, voluntario=voluntario).exists():
                return Response({"detail": "Ya estás inscripto en esta capacitación."}, status=status.HTTP_400_BAD_REQUEST)

            # cupo
            if cap_locked.cupo:
                inscritos = InscripcionCapacitacion.objects.filter(capacitacion=cap).count()
                if inscritos >= cap_locked.cupo:
                    return Response({"detail": "La capacitación ya alcanzó su cupo máximo."}, status=status.HTTP_400_BAD_REQUEST)

            ins = InscripcionCapacitacion.objects.create(capacitacion=cap, voluntario=voluntario)
            ser = InscripcionCapacitacionSerializer(ins, context={"request": request})
            return Response(ser.data, status=status.HTTP_201_CREATED)


class InscripcionCapacitacionViewSet(viewsets.ModelViewSet):
    """
    CRUD para inscripciones (solo para Gestores).
    Permite a los gestores listar, ver, editar y eliminar inscripciones a capacitaciones.
    """
    queryset = InscripcionCapacitacion.objects.select_related("capacitacion", "voluntario__persona").all()
    serializer_class = InscripcionCapacitacionSerializer
    permission_classes = [IsGestionador]  # Solo gestores pueden gestionar inscripciones
