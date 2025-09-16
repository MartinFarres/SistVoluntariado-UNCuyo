from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Capacitacion, InscripcionCapacitacion
from .serializers import CapacitacionSerializer, InscripcionCapacitacionSerializer
from apps.persona.models import Voluntario

class CapacitacionViewSet(viewsets.ModelViewSet):
    """
    CRUD de capacitaciones.
    - GET /capacitaciones/         -> list
    - POST /capacitaciones/        -> create
    - GET /capacitaciones/{pk}/    -> retrieve
    - PUT/PATCH /capacitaciones/{pk}/ -> update
    - DELETE /capacitaciones/{pk}/ -> destroy
    - POST /capacitaciones/{pk}/inscribirse/ -> acción custom para inscribirse
    """
    queryset = Capacitacion.objects.select_related("voluntariado").all()
    serializer_class = CapacitacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # si tu modelo tuviera creado_por, lo podríamos setear aquí:
        # serializer.save(creado_por=self.request.user)
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
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
        except persona.DoesNotExist:
            return Response({"detail": "La persona no está registrada como persona."}, status=status.HTTP_400_BAD_REQUEST)

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
    CRUD para inscripciones (si querés que admins puedan listar/editar aprobaciones, etc).
    """
    queryset = InscripcionCapacitacion.objects.select_related("capacitacion", "voluntario__persona").all()
    serializer_class = InscripcionCapacitacionSerializer
    permission_classes = [permissions.IsAuthenticated]  # ajustar permisos según política
