from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q, Min, Max
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado, InscripcionConvocatoria
from .serializers import VoluntariadoSerializer, TurnoSerializer, InscripcionTurnoSerializer, DescripcionVoluntariadoSerializer, InscripcionConvocatoriaSerializer
from apps.users.permissions import IsAdministrador, IsGestionador
from apps.persona.models import Voluntario
from rest_framework import serializers
from django.db import transaction

class VoluntariadoViewSet(viewsets.ModelViewSet):
    # No prefetch del reverse relation 'turno_set' (puede no existir según related_name).
    # Si se necesita prefetch de turnos, usar el endpoint `turnos` que consulta Turno directamente.
    queryset = Voluntariado.objects.select_related("descripcion").all()
    serializer_class = VoluntariadoSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "list", "turnos"):
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action in ["mis_voluntariados", "progreso", "asistencia_completa"]:
            return [permissions.IsAuthenticated(), IsGestionador()]

        elif self.action == "turnos":
            return [permissions.IsAuthenticatedOrReadOnly()]
        else:
            return [permissions.IsAuthenticated(), IsAdministrador()]

    def get_queryset(self):
        """
        Filtra voluntariados por estado temporal basado en fecha_inicio y fecha_fin.
        
        Query params:
        - status: 'upcoming' (no han empezado), 'active' (en progreso), 'finished' (finalizados)
        """
        queryset = super().get_queryset()
        # Anotar cantidad de turnos activos para cada voluntariado (sin filtrar resultados)
        queryset = queryset.annotate(
            turnos_count=Count('turnos', filter=Q(turnos__is_active=True)),
            # Calcular fechas a partir de los turnos activos
            fecha_inicio=Min('turnos__fecha', filter=Q(turnos__is_active=True)),
            fecha_fin=Max('turnos__fecha', filter=Q(turnos__is_active=True)),
        )
        status_filter = self.request.query_params.get('status', None)
        
        if status_filter:
            now = timezone.now().date()
                
            # Mantener solo voluntariados que tengan al menos un turno activo
            queryset = queryset.annotate(
                num_turnos=Count('turnos', filter=Q(turnos__is_active=True))
            ).filter(num_turnos__gt=0)

            if status_filter == 'upcoming':
                # Voluntariados que aún no han comenzado (inicio > hoy)
                queryset = queryset.filter(fecha_inicio__gt=now)
            elif status_filter == 'active':
                # Voluntariados en progreso (inicio <= hoy <= fin)
                queryset = queryset.filter(fecha_inicio__lte=now, fecha_fin__gte=now)
            elif status_filter == 'finished':
                # Voluntariados finalizados (fin < hoy)
                queryset = queryset.filter(fecha_fin__lt=now)
        
        return queryset
    
    @action(detail=False, methods=["get"], url_path='all-valid', permission_classes=[permissions.IsAuthenticated, IsGestionador])
    def get_all_valid(self, request):
        """
        Lista de voluntariados válidos (con al menos un turno activo),
        disponible para roles de gestionador.
        """
        queryset = self.get_queryset()
        # Mantener solo voluntariados que tengan al menos un turno activo
        queryset = queryset.annotate(
            num_turnos=Count('turnos', filter=Q(turnos__is_active=True))
        ).filter(num_turnos__gt=0)

        # Paginación estándar del ViewSet
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path='mis-voluntariados', permission_classes=[permissions.IsAuthenticated, IsGestionador])
    def mis_voluntariados(self, request):
        """
        Retorna los voluntariados gestionados por el Gestionador actual (Delegado/Administrativo).
        Para Administradores, retorna TODOS los voluntariados.
        Incluye el conteo de voluntarios inscritos activos en cada voluntariado.

        Query params:
        - status: 'upcoming' (no han empezado), 'active' (en progreso), 'finished' (finalizados)
          Si no se especifica, retorna todos los voluntariados con estado ACTIVE.

        Endpoint: GET /voluntariados/mis-voluntariados/?status=active
        """
        user = request.user
        role = getattr(user, 'role', '')
        
        # Si es ADMIN, retornar todos los voluntariados sin filtrar por organización
        if role == 'ADMIN':
            queryset = self.get_queryset()
        elif role == 'DELEG':
            # Para Delegados/Administrativos, filtrar por organización
            persona = getattr(user, "persona", None)
            if not persona:
                return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener la instancia de gestionador (Delegado/Administrativo). Cualquiera sirve porque heredan de Gestionador.
            gestionador_obj = persona.gestionador.delegado

            # Get the gestionador's organization
            gestionador_org = getattr(gestionador_obj, 'organizacion', None) if hasattr(gestionador_obj, 'organizacion') else None
            
            if gestionador_org is None:
                # If gestionador has no organization, return empty queryset
                return Response({"detail": "El gestionador no tiene una organización asignada."}, status=status.HTTP_400_BAD_REQUEST)

            # Filter voluntariados where organization matches gestionador's organization
            queryset = self.get_queryset().filter(organizacion=gestionador_org)
        else:
            return Response({"detail": "La persona no es un gestionador válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mantener solo voluntariados que tengan al menos un turno activo
        queryset = queryset.annotate(
            num_turnos=Count('turnos', filter=Q(turnos__is_active=True))
        ).filter(num_turnos__gt=0)

        # Aplicar filtro de status temporal si se proporciona
        status_filter = request.query_params.get('status', None)
        if status_filter:
            now = timezone.now().date()
            
            if status_filter == 'upcoming':
                # Voluntariados que aún no han comenzado (fecha_inicio > hoy)
                queryset = queryset.filter(fecha_inicio__gt=now)
            elif status_filter == 'active':
                # Voluntariados en progreso (fecha_inicio <= hoy <= fecha_fin)
                queryset = queryset.filter(fecha_inicio__lte=now, fecha_fin__gte=now)
            elif status_filter == 'finished':
                # Voluntariados finalizados (fecha_fin < hoy)
                queryset = queryset.filter(fecha_fin__lt=now)

        # Anotar el conteo de voluntarios inscritos (estados INSCRITO y ASISTIO)
        queryset = queryset.annotate(
            voluntarios_count=Count(
                'turnos__inscripciones',
                filter=Q(
                    turnos__inscripciones__estado__in=[
                        InscripcionTurno.Status.INSCRITO,
                        InscripcionTurno.Status.ASISTIO
                    ]
                ),
                distinct=True
            )
        )

        # Ordenar por fecha de inicio (más cercanos primero para upcoming, más recientes primero para active/finished)
        if status_filter == 'upcoming':
            queryset = queryset.order_by('fecha_inicio')
        else:
            queryset = queryset.order_by('-fecha_inicio')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def turnos(self, request, pk=None):
        """
        Devuelve la lista de turnos pertenecientes a este voluntariado.
        Endpoint: GET /voluntariados/{pk}/turnos/
        """
        voluntariado = get_object_or_404(Voluntariado, pk=pk)
        # Filtrar turnos por voluntariado; no usar select_related('voluntariado') ya que puede no existir esa relación por nombre
        turnos_qs = Turno.objects.filter(voluntariado_id=voluntariado.id).annotate(
            inscripciones_count=Count(
                'inscripciones',
                filter=Q(
                    inscripciones__estado__in=[
                        InscripcionTurno.Status.INSCRITO,
                        InscripcionTurno.Status.ASISTIO
                    ]
                ),
                distinct=True
            )
        )
        ser = TurnoSerializer(turnos_qs, many=True, context={"request": request})
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path='progreso', permission_classes=[permissions.IsAuthenticated, IsGestionador])
    def progreso(self, request, pk=None):
        """
        Calcula el progreso del voluntariado basado en sus turnos.

        Definición de progreso: porcentaje de turnos finalizados respecto del total de turnos programados.
        - Un turno se considera finalizado si fecha < hoy o (fecha == hoy y hora_fin <= ahora).

        Endpoint: GET /voluntariados/{pk}/progreso/
        Respuesta: {
          voluntariado: <id>,
          total_turnos: <int>,
          turnos_finalizados: <int>,
          progreso: <int 0-100>
        }
        """
        voluntariado = get_object_or_404(Voluntariado, pk=pk)

        # Autorización adicional: si no es ADMIN, debe pertenecer a la misma organización del voluntariado
        user = request.user
        role = getattr(user, 'role', '')
        if role not in ['ADMIN']:
            persona = getattr(user, 'persona', None)
            gestionador_obj = None
            if persona is not None:
                if hasattr(persona, 'delegado') and persona.delegado is not None:
                    gestionador_obj = persona.delegado
                elif hasattr(persona, 'administrativo') and persona.administrativo is not None:
                    gestionador_obj = persona.administrativo
                elif hasattr(persona, 'gestionador') and persona.gestionador is not None:
                    gestionador_obj = persona.gestionador
            
            # Check if gestionador's organization matches voluntariado's organization
            if gestionador_obj is None:
                return Response({"detail": "No tiene permisos para ver el progreso de este voluntariado."}, status=status.HTTP_403_FORBIDDEN)
            
            gestionador_org = getattr(gestionador_obj, 'organizacion', None) if hasattr(gestionador_obj, 'organizacion') else None
            voluntariado_org = voluntariado.organizacion
            
            # If voluntariado has no organization, deny access to non-admin gestionadores
            # If gestionador has no organization, deny access
            # Otherwise, check if organizations match
            if voluntariado_org is None or gestionador_org is None or gestionador_org.id != voluntariado_org.id:
                return Response({"detail": "No tiene permisos para ver el progreso de este voluntariado."}, status=status.HTTP_403_FORBIDDEN)

        # Get current datetime and convert to local timezone
        now = timezone.now()
        now_local = timezone.localtime(now)
        today = now_local.date()
        time_now = now_local.time()

        # Only count active (non-deleted) turnos
        total_turnos = Turno.objects.filter(voluntariado_id=voluntariado.id, is_active=True).count()
        turnos_finalizados = Turno.objects.filter(
            voluntariado_id=voluntariado.id, 
            is_active=True
        ).filter(
            Q(fecha__lt=today) | (Q(fecha=today) & Q(hora_fin__lte=time_now))
        ).count()

        progreso = 0
        if total_turnos > 0:
            progreso = int((turnos_finalizados / total_turnos) * 100)

        # Get turnos info for debugging
        turnos_info = []
        for turno in Turno.objects.filter(voluntariado_id=voluntariado.id, is_active=True):
            is_finished = turno.fecha < today or (turno.fecha == today and turno.hora_fin <= time_now)
            turnos_info.append({
                'id': turno.id,
                'fecha': str(turno.fecha),
                'hora_fin': str(turno.hora_fin),
                'is_finished': is_finished
            })

        data = {
            'voluntariado': voluntariado.id,
            'total_turnos': total_turnos,
            'turnos_finalizados': turnos_finalizados,
            'progreso': progreso,
            'today': str(today),
            'time_now': str(time_now),
            'turnos_debug': turnos_info
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path='asistencia-completa', permission_classes=[permissions.IsAuthenticated, IsGestionador])
    def asistencia_completa(self, request, pk=None):
        """
        Verifica si todas las asistencias han sido registradas para un voluntariado finalizado.
        
        Endpoint: GET /voluntariados/{pk}/asistencia-completa/
        Respuesta: {
          voluntariado: <id>,
          total_inscripciones: <int>,
          asistencias_registradas: <int>,
          completa: <bool>,
          porcentaje_completitud: <int 0-100>
        }
        """
        from apps.asistencia.models import Asistencia
        
        voluntariado = get_object_or_404(Voluntariado, pk=pk)

        # Autorización adicional: si no es ADMIN, debe pertenecer a la misma organización del voluntariado
        user = request.user
        role = getattr(user, 'role', '')
        if role not in ['ADMIN']:
            persona = getattr(user, 'persona', None)
            gestionador_obj = None
            if persona is not None:
                if hasattr(persona, 'delegado') and persona.delegado is not None:
                    gestionador_obj = persona.delegado
                elif hasattr(persona, 'administrativo') and persona.administrativo is not None:
                    gestionador_obj = persona.administrativo
                elif hasattr(persona, 'gestionador') and persona.gestionador is not None:
                    gestionador_obj = persona.gestionador
            
            # Check if gestionador's organization matches voluntariado's organization
            if gestionador_obj is None:
                return Response({"detail": "No tiene permisos para ver la información de asistencia de este voluntariado."}, status=status.HTTP_403_FORBIDDEN)
            
            gestionador_org = getattr(gestionador_obj, 'organizacion', None) if hasattr(gestionador_obj, 'organizacion') else None
            voluntariado_org = voluntariado.organizacion
            
            # If voluntariado has no organization, deny access to non-admin gestionadores
            # If gestionador has no organization, deny access
            # Otherwise, check if organizations match
            if voluntariado_org is None or gestionador_org is None or gestionador_org.id != voluntariado_org.id:
                return Response({"detail": "No tiene permisos para ver la información de asistencia de este voluntariado."}, status=status.HTTP_403_FORBIDDEN)

        # Contar todas las inscripciones activas (INSCRITO y ASISTIO) en turnos finalizados
        now = timezone.now()
        now_local = timezone.localtime(now)
        today = now_local.date()
        time_now = now_local.time()

        # Obtener turnos finalizados
        turnos_finalizados = Turno.objects.filter(
            voluntariado_id=voluntariado.id,
            is_active=True
        ).filter(
            Q(fecha__lt=today) | (Q(fecha=today) & Q(hora_fin__lte=time_now))
        )

        # Contar inscripciones en esos turnos
        total_inscripciones = InscripcionTurno.objects.filter(
            turno__in=turnos_finalizados,
            is_active=True,
            estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO]
        ).count()

        # Contar cuántas tienen asistencia registrada
        asistencias_registradas = Asistencia.objects.filter(
            inscripcion__turno__in=turnos_finalizados,
            inscripcion__is_active=True,
            is_active=True
        ).count()

        completa = total_inscripciones > 0 and asistencias_registradas >= total_inscripciones
        porcentaje_completitud = 0
        if total_inscripciones > 0:
            porcentaje_completitud = int((asistencias_registradas / total_inscripciones) * 100)

        data = {
            'voluntariado': voluntariado.id,
            'total_inscripciones': total_inscripciones,
            'asistencias_registradas': asistencias_registradas,
            'completa': completa,
            'porcentaje_completitud': porcentaje_completitud
        }
        return Response(data, status=status.HTTP_200_OK)


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

            # Check if voluntario has an active inscription to the voluntariado
            voluntariado = turno.voluntariado
            has_convocatoria_inscription = InscripcionConvocatoria.objects.filter(
                voluntariado=voluntariado,
                voluntario=voluntario,
                estado__in=[InscripcionConvocatoria.Status.INSCRITO, InscripcionConvocatoria.Status.ACEPTADO],
                is_active=True
            ).exists()
            
            if not has_convocatoria_inscription:
                return Response({"detail": "Debes estar inscripto en el voluntariado antes de inscribirte a un turno."}, status=status.HTTP_400_BAD_REQUEST)

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
        role = getattr(user, 'role', '')
        is_admin_or_staff = bool(getattr(user, 'is_staff', False) or role == 'ADMIN')
        is_gestionador = role in ['ADMIN', 'DELEG']

        # Volunteers can only see their own inscriptions
        if user.is_authenticated and not (is_admin_or_staff or is_gestionador):
            if hasattr(user, 'persona') and hasattr(user.persona, 'voluntario'):
                queryset = queryset.filter(voluntario=user.persona.voluntario)
            else:
                return queryset.none()
        
        voluntario_id = self.request.query_params.get('voluntario_id')
        if voluntario_id and is_admin_or_staff:
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


class InscripcionConvocatoriaViewSet(viewsets.ModelViewSet):
    queryset = InscripcionConvocatoria.objects.select_related("voluntariado", "voluntario__persona_ptr").all()
    serializer_class = InscripcionConvocatoriaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        role = getattr(user, 'role', '')
        is_admin_or_staff = bool(getattr(user, 'is_staff', False) or role == 'ADMIN')
        is_gestionador = role in ['ADMIN', 'DELEG']

        # Volunteers can only see their own inscriptions
        if user.is_authenticated and not (is_admin_or_staff or is_gestionador):
            if hasattr(user, 'persona') and hasattr(user.persona, 'voluntario'):
                queryset = queryset.filter(voluntario=user.persona.voluntario)
            else:
                return queryset.none()
        
        # Filter by voluntario_id if provided (admin/gestionador only)
        voluntario_id = self.request.query_params.get('voluntario_id')
        if voluntario_id and (is_admin_or_staff or is_gestionador):
            queryset = queryset.filter(voluntario_id=voluntario_id)

        # Filter by voluntariado_id if provided
        voluntariado_id = self.request.query_params.get('voluntariado_id', None)
        if voluntariado_id is not None:
            queryset = queryset.filter(voluntariado__id=voluntariado_id)
        
        # Filter by estado if provided
        estado = self.request.query_params.get('estado', None)
        if estado is not None:
            queryset = queryset.filter(estado=estado)
            
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
    
    @action(detail=False, methods=["post"], url_path='inscribirse')
    def inscribirse(self, request):
        """
        Permite a un voluntario inscribirse a un voluntariado.
        Endpoint: POST /voluntariado/inscripciones-convocatoria/inscribirse/
        Body: { "voluntariado_id": <int> }
        """
        persona = getattr(request.user, "persona", None)
        if not persona:
            return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            voluntario = persona.voluntario
        except Voluntario.DoesNotExist:
            return Response({"detail": "La persona no está registrada como voluntario."}, status=status.HTTP_400_BAD_REQUEST)

        voluntariado_id = request.data.get('voluntariado_id')
        if not voluntariado_id:
            return Response({"detail": "El campo 'voluntariado_id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            voluntariado = Voluntariado.objects.get(pk=voluntariado_id, is_active=True)
        except Voluntariado.DoesNotExist:
            return Response({"detail": "Voluntariado no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Check if voluntariado is in "Convocatoria" stage
        today = timezone.now().date()
        
        if not voluntariado.fecha_inicio_convocatoria or not voluntariado.fecha_fin_convocatoria:
            return Response(
                {"detail": "El voluntariado no tiene fechas de convocatoria configuradas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if today < voluntariado.fecha_inicio_convocatoria:
            return Response(
                {"detail": "La convocatoria para este voluntariado aún no ha comenzado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if today > voluntariado.fecha_fin_convocatoria:
            return Response(
                {"detail": "La convocatoria para este voluntariado ya ha finalizado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already inscribed
        existing = InscripcionConvocatoria.objects.filter(
            voluntariado=voluntariado,
            voluntario=voluntario,
            estado=InscripcionConvocatoria.Status.INSCRITO,
            is_active=True
        ).first()
        
        if existing:
            return Response({"detail": "Ya estás inscripto en este voluntariado."}, status=status.HTTP_400_BAD_REQUEST)

        # Create inscription
        inscripcion = InscripcionConvocatoria.objects.create(
            voluntariado=voluntariado,
            voluntario=voluntario,
            estado=InscripcionConvocatoria.Status.INSCRITO
        )
        
        serializer = self.get_serializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["post"], url_path='cancelar')
    def cancelar(self, request, pk=None):
        """
        Permite a un voluntario cancelar su inscripción a un voluntariado.
        Endpoint: POST /voluntariado/inscripciones-convocatoria/{pk}/cancelar/
        """
        inscripcion = get_object_or_404(InscripcionConvocatoria, pk=pk)
        
        # Check permissions
        persona = getattr(request.user, "persona", None)
        if not persona or not hasattr(persona, 'voluntario'):
            return Response({"detail": "Usuario sin persona asociada."}, status=status.HTTP_400_BAD_REQUEST)
        
        voluntario = persona.voluntario
        
        # Only the owner or admin can cancel
        role = getattr(request.user, 'role', '')
        if inscripcion.voluntario.id != voluntario.id and role not in ['ADMIN', 'DELEG']:
            return Response({"detail": "No tienes permisos para cancelar esta inscripción."}, status=status.HTTP_403_FORBIDDEN)
        
        inscripcion.estado = InscripcionConvocatoria.Status.CANCELADO
        inscripcion.save()
        
        serializer = self.get_serializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], url_path='aceptar', permission_classes=[permissions.IsAuthenticated, IsGestionador])
    def aceptar(self, request, pk=None):
        """
        Permite a un gestionador aceptar una inscripción a un voluntariado.
        Endpoint: POST /voluntariado/inscripciones-convocatoria/{pk}/aceptar/
        """
        inscripcion = get_object_or_404(InscripcionConvocatoria, pk=pk)
        
        if inscripcion.estado != InscripcionConvocatoria.Status.INSCRITO:
            return Response({"detail": "Solo se pueden aceptar inscripciones en estado INSCRITO."}, status=status.HTTP_400_BAD_REQUEST)
        
        inscripcion.estado = InscripcionConvocatoria.Status.ACEPTADO
        inscripcion.save()
        
        serializer = self.get_serializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], url_path='rechazar', permission_classes=[permissions.IsAuthenticated, IsGestionador])
    def rechazar(self, request, pk=None):
        """
        Permite a un gestionador rechazar una inscripción a un voluntariado.
        Endpoint: POST /voluntariado/inscripciones-convocatoria/{pk}/rechazar/
        """
        inscripcion = get_object_or_404(InscripcionConvocatoria, pk=pk)
        
        if inscripcion.estado != InscripcionConvocatoria.Status.INSCRITO:
            return Response({"detail": "Solo se pueden rechazar inscripciones en estado INSCRITO."}, status=status.HTTP_400_BAD_REQUEST)
        
        inscripcion.estado = InscripcionConvocatoria.Status.RECHAZADO
        inscripcion.save()
        
        serializer = self.get_serializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_200_OK)
