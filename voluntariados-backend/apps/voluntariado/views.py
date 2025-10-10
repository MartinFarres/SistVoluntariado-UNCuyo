from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado
from .serializers import VoluntariadoSerializer, TurnoSerializer, InscripcionTurnoSerializer, DescripcionVoluntariadoSerializer

class VoluntariadoViewSet(viewsets.ModelViewSet):
    queryset = Voluntariado.objects.select_related("descripcion", "gestionadores").all()
    serializer_class = VoluntariadoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class DescripcionVoluntariadoViewSet(viewsets.ModelViewSet):
    queryset = DescripcionVoluntariado.objects.all()
    serializer_class = DescripcionVoluntariadoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def inscribirse(self, request, pk=None):
        """
        Acción custom para que el usuario actual se inscriba en el turno.
        Requiere que el usuario tenga un Voluntario asociado (request.user.persona.voluntario).
        """
        turno = get_object_or_404(Turno, pk=pk)
        # obtener voluntario del usuario
        persona = getattr(request.user, "persona", None)
        if not persona:
            return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            voluntario = persona.voluntario
        except persona.DoesNotExist:
            return Response({"detail": "La persona no está registrada como persona."}, status=status.HTTP_400_BAD_REQUEST)

        # verificar cupo y existencia (mismo chequeo que el serializer)
        activos = turno.inscripciones.filter(estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO]).count()
        if activos >= turno.cupo:
            return Response({"detail": "El turno ya está completo."}, status=status.HTTP_400_BAD_REQUEST)

        if InscripcionTurno.objects.filter(turno=turno, voluntario=voluntario).exists():
            return Response({"detail": "Ya estás inscripto en este turno."}, status=status.HTTP_400_BAD_REQUEST)

        inscripcion = InscripcionTurno.objects.create(turno=turno, voluntario=voluntario)
        ser = InscripcionTurnoSerializer(inscripcion, context={"request": request})
        return Response(ser.data, status=status.HTTP_201_CREATED)

class InscripcionTurnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InscripcionTurno.objects.select_related("turno", "voluntario__persona").all()
    serializer_class = InscripcionTurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por turno si se proporciona
        turno_id = self.request.query_params.get('turno', None)
        if turno_id is not None:
            queryset = queryset.filter(turno__id=turno_id)
        return queryset
    def perform_create(self, serializer):
        # Asignar el voluntario del usuario actual al crear la inscripción
        persona = getattr(self.request.user, "persona", None)
        if not persona:
            raise ValueError("Usuario sin persona asociada.")
        try:
            voluntario = persona.voluntario
        except persona.DoesNotExist:
            raise ValueError("La persona no está registrada como persona.")
        
        serializer.save(voluntario=voluntario)
    