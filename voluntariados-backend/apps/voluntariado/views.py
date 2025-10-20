from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado
from .serializers import VoluntariadoSerializer, TurnoSerializer, InscripcionTurnoSerializer, DescripcionVoluntariadoSerializer
from apps.users.permissions import IsAdministrador
from apps.persona.models import Voluntario
from rest_framework import serializers
from django.db import transaction

class VoluntariadoViewSet(viewsets.ModelViewSet):
    # No prefetch del reverse relation 'turno_set' (puede no existir según related_name).
    # Si se necesita prefetch de turnos, usar el endpoint `turnos` que consulta Turno directamente.
    queryset = Voluntariado.objects.select_related("descripcion").prefetch_related("gestionadores").all()
    serializer_class = VoluntariadoSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "list"):
            return [permissions.IsAuthenticatedOrReadOnly()]
        else:
            return [permissions.IsAuthenticated(), IsAdministrador()]

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def turnos(self, request, pk=None):
        """
        Devuelve la lista de turnos pertenecientes a este voluntariado.
        Endpoint: GET /voluntariados/{pk}/turnos/
        """
        voluntariado = get_object_or_404(Voluntariado, pk=pk)
        # Filtrar turnos por voluntariado; no usar select_related('voluntariado') ya que puede no existir esa relación por nombre
        turnos_qs = Turno.objects.filter(voluntariado_id=voluntariado.id)
        ser = TurnoSerializer(turnos_qs, many=True, context={"request": request})
        return Response(ser.data, status=status.HTTP_200_OK)


class DescripcionVoluntariadoViewSet(viewsets.ModelViewSet):
    queryset = DescripcionVoluntariado.objects.all()
    serializer_class = DescripcionVoluntariadoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TurnoViewSet(viewsets.ModelViewSet):
    # Usar queryset simple; evitar select_related('voluntariado') si el campo FK tiene otro nombre
    queryset = Turno.objects.select_related("voluntariado").all()
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        voluntariado_id = self.request.query_params.get("voluntariado")
        if voluntariado_id:
            queryset = queryset.filter(voluntariado_id=voluntariado_id)
        return queryset

    @action(detail=True, methods=["post"], url_path='cancelar-inscripcion', permission_classes=[permissions.IsAuthenticated])
    def cancelar_inscripcion(self, request, pk=None):
        turno = get_object_or_404(Turno, pk=pk)
        persona = getattr(request.user, "persona", None)
        if not persona:
            return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            voluntario = persona.voluntario
        except Voluntario.DoesNotExist:
            return Response({"detail": "La persona no está registrada como voluntario."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inscripcion = InscripcionTurno.objects.get(turno=turno, voluntario=voluntario, is_active=True)
            inscripcion.estado = InscripcionTurno.Status.CANCELADO
            inscripcion.save()  
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InscripcionTurno.DoesNotExist:
            return Response({"detail": "No se encontró una inscripción activa para este turno y usuario."}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def inscribirse(self, request, pk=None):
        # obtener voluntario del usuario
        persona = getattr(request.user, "persona", None)
        if not persona:
            return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            voluntario = persona.voluntario
        except Voluntario.DoesNotExist:
            return Response({"detail": "La persona no está registrada como voluntario."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # bloquear el turno para evitar race conditions en cupo
            try:
                turno = Turno.objects.select_for_update().get(pk=pk)
            except Turno.DoesNotExist:
                return Response({"detail": "Turno no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # contar inscripciones activas (INSCRITO / ASISTIO)
            activos = turno.inscripciones.filter(
                estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO]
            ).count()

            # intentar obtener una inscripción preexistente (bloqueada)
            try:
                inscripcion = InscripcionTurno.objects.select_for_update().get(turno=turno, voluntario=voluntario)
            except InscripcionTurno.DoesNotExist:
                inscripcion = None

            # Si ya existe y está activa -> error
            if inscripcion and inscripcion.estado in (InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO):
                return Response({"detail": "Ya estás inscripto en este turno."}, status=status.HTTP_400_BAD_REQUEST)

            # Si existe pero estaba cancelada -> reactivar si hay cupo
            if inscripcion and inscripcion.estado == InscripcionTurno.Status.CANCELADO:
                if activos >= turno.cupo:
                    return Response({"detail": "El turno ya está completo."}, status=status.HTTP_400_BAD_REQUEST)
                inscripcion.estado = InscripcionTurno.Status.INSCRITO
                # si tenés campos como 'canceled_at' o similar, resetealos aquí
                inscripcion.save()
                ser = InscripcionTurnoSerializer(inscripcion, context={"request": request})
                return Response(ser.data, status=status.HTTP_200_OK)

            # No había inscripción previa: crear nueva si hay cupo
            if activos >= turno.cupo:
                return Response({"detail": "El turno ya está completo."}, status=status.HTTP_400_BAD_REQUEST)

            nueva = InscripcionTurno.objects.create(turno=turno, voluntario=voluntario)
            ser = InscripcionTurnoSerializer(nueva, context={"request": request})
            return Response(ser.data, status=status.HTTP_201_CREATED)

class InscripcionTurnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InscripcionTurno.objects.select_related("turno", "voluntario__persona_ptr").all()
    serializer_class = InscripcionTurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_authenticated and not (user.is_staff or getattr(user, 'role', '') == 'ADMIN'):
            if hasattr(user, 'persona') and hasattr(user.persona, 'voluntario'):
                queryset = queryset.filter(voluntario=user.persona.voluntario)
            else:
                return queryset.none()
        
        voluntario_id = self.request.query_params.get('voluntario_id')
        if voluntario_id and (user.is_staff or getattr(user, 'role', '') == 'ADMIN'):
             queryset = queryset.filter(voluntario_id=voluntario_id)

        turno_id = self.request.query_params.get('turno', None)
        if turno_id is not None:
            queryset = queryset.filter(turno__id=turno_id)
        return queryset

   

    def perform_create(self, serializer):
        persona = getattr(self.request.user, "persona", None)
        if not persona:
            raise serializers.ValidationError("Usuario sin persona asociada.")
        try:
            voluntario = persona.voluntario
        except Voluntario.DoesNotExist:
            raise serializers.ValidationError("El usuario no es un voluntario registrado.")
        
        serializer.save(voluntario=voluntario)
