from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado, InscripcionConvocatoria
from apps.persona.models import Voluntario, Gestionador

from ..persona.serializers import GestionadorSerializer, VoluntarioSerializer
from ..organizacion.serializers import OrganizacionSerializer
from ..organizacion.models import Organizacion


class DescripcionVoluntariadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescripcionVoluntariado
        fields = ("id", "descripcion", "logo", "portada", "resumen")
        read_only_fields = ("id",)

class TurnoSerializer(serializers.ModelSerializer):
    voluntariado = serializers.StringRelatedField(read_only=True) #lectura
    voluntariado_id = serializers.PrimaryKeyRelatedField( #escritura
        queryset=Voluntariado.objects.all(),
        source='voluntariado',
        write_only=True,
        required=True,
        allow_null=True
    )
    # Campo de solo lectura para exponer cantidad de inscripciones activas
    inscripciones_count = serializers.IntegerField(read_only=True, required=False)
    class Meta:
        model = Turno
        fields = ("id", "fecha", "hora_inicio", "hora_fin", "cupo", "lugar","voluntariado","voluntariado_id", "inscripciones_count")
        read_only_fields = ("id",)

class VoluntariadoSerializer(serializers.ModelSerializer):
    # --- Campos para Lectura ---

    # Fechas calculadas desde los turnos (anotaciones en queryset)
    fecha_inicio = serializers.DateField(read_only=True)
    fecha_fin = serializers.DateField(read_only=True)

    descripcion = DescripcionVoluntariadoSerializer(read_only=True)
    voluntarios_count = serializers.IntegerField(read_only=True, required=False)
    turnos_count = serializers.IntegerField(read_only=True, required=False)
    organizacion = OrganizacionSerializer(read_only=True)
    etapa = serializers.SerializerMethodField()
    
    descripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=DescripcionVoluntariado.objects.all(), source='descripcion', write_only=True, required=False, allow_null=True
    )

    organizacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Organizacion.objects.all(), source='organizacion', write_only=True, required=False, allow_null=True
    )


    class Meta:
        model = Voluntariado
        fields = (
            'id', 'nombre', 'fecha_inicio', 'fecha_fin', 'organizacion',
            'fecha_inicio_convocatoria', 'fecha_fin_convocatoria',
            'fecha_inicio_cursado', 'fecha_fin_cursado',
            'etapa',  # Campo calculado
            'descripcion',    # Campo de lectura (objeto anidado)
            'voluntarios_count',  # Campo de lectura (anotación)
            'turnos_count',       # Campo de lectura (anotación)
            'descripcion_id', # Campo de escritura
            'organizacion_id'
        )
        extra_kwargs = {}

    def get_etapa(self, obj):
        """
        Calcula la etapa actual del voluntariado basándose en las fechas:
        - Proximamente: Antes de la convocatoria
        - Convocatoria: Durante el período de convocatoria
        - Preparación: Entre el fin de convocatoria y el inicio de cursado
        - Activo: Durante el período de cursado
        - Finalizado: Después del período de cursado
        """
        today = timezone.now().date()
        
        # Si no hay fechas de convocatoria, no se puede determinar la etapa
        if not obj.fecha_inicio_convocatoria or not obj.fecha_fin_convocatoria:
            return None
        
        # Proximamente: Antes de la convocatoria
        if today < obj.fecha_inicio_convocatoria:
            return "Proximamente"
        
        # Convocatoria: Durante el período de convocatoria
        if obj.fecha_inicio_convocatoria <= today <= obj.fecha_fin_convocatoria:
            return "Convocatoria"
        
        # Si no hay fechas de cursado pero ya pasó la convocatoria
        if not obj.fecha_inicio_cursado or not obj.fecha_fin_cursado:
            # Si ya pasó la convocatoria, considerarlo finalizado
            if today > obj.fecha_fin_convocatoria:
                return "Finalizado"
            return None
        
        # Preparación: Entre convocatoria y cursado
        if obj.fecha_fin_convocatoria < today < obj.fecha_inicio_cursado:
            return "Preparación"
        
        # Activo: Durante el período de cursado
        if obj.fecha_inicio_cursado <= today <= obj.fecha_fin_cursado:
            return "Activo"
        
        # Finalizado: Después del período de cursado
        if today > obj.fecha_fin_cursado:
            return "Finalizado"
        
        # No debería llegar aquí con validaciones correctas
        return None

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate(self, data):
        """
        Check that fecha_fin is not earlier than fecha_inicio.
        Check that convocatoria and cursado dates are logical.
        """
        if data.get('fecha_inicio') and data.get('fecha_fin') and data['fecha_inicio'] > data['fecha_fin']:
            raise serializers.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        
        # Validation 2: Start date should be before end date for both stages
        # Validate convocatoria dates
        if data.get('fecha_inicio_convocatoria') and data.get('fecha_fin_convocatoria'):
            if data['fecha_inicio_convocatoria'] > data['fecha_fin_convocatoria']:
                raise serializers.ValidationError(
                    "La fecha de fin de convocatoria no puede ser anterior a la fecha de inicio de convocatoria."
                )
        
        # Validate cursado dates
        if data.get('fecha_inicio_cursado') and data.get('fecha_fin_cursado'):
            if data['fecha_inicio_cursado'] > data['fecha_fin_cursado']:
                raise serializers.ValidationError(
                    "La fecha de fin de cursado no puede ser anterior a la fecha de inicio de cursado."
                )
        
        # Validation 1: Convocatoria must be before cursado and should not overlap
        if data.get('fecha_fin_convocatoria') and data.get('fecha_inicio_cursado'):
            if data['fecha_fin_convocatoria'] >= data['fecha_inicio_cursado']:
                raise serializers.ValidationError(
                    "La fecha de fin de convocatoria debe ser anterior a la fecha de inicio de cursado. "
                    "Las etapas no deben superponerse."
                )
        
        return data

class TurnoParaVoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ("id", "fecha", "hora_inicio", "hora_fin", "lugar")

class VoluntariadoConTurnosSerializer(VoluntariadoSerializer):
    turnos = serializers.SerializerMethodField()
    organizacion_nombre = serializers.CharField(source='organizacion.nombre', read_only=True)


    class Meta(VoluntariadoSerializer.Meta):
        fields = VoluntariadoSerializer.Meta.fields + ('turnos', 'organizacion_nombre')
    
    def get_turnos(self, obj):
        voluntario_id = self.context.get('voluntario_id')
        if voluntario_id:
            # Get turnos for this voluntariado where the specific voluntario is inscribed
            inscripciones = InscripcionTurno.objects.filter(
                voluntario_id=voluntario_id, 
                turno__voluntariado=obj,
                estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO]
            ).select_related('turno')
            turnos = [inscripcion.turno for inscripcion in inscripciones]
            return TurnoParaVoluntarioSerializer(turnos, many=True).data
        # Fallback if no voluntario_id is provided (e.g. for general admin views)
        return TurnoSerializer(obj.turnos.all(), many=True).data


class InscripcionTurnoSerializer(serializers.ModelSerializer):
    # Nested read fields
    voluntario = VoluntarioSerializer(read_only=True)
    # Write-only fields
    voluntario_id = serializers.PrimaryKeyRelatedField(
        queryset=Voluntario.objects.all(), source='voluntario', write_only=True, required=False
    )
    turno_id = serializers.PrimaryKeyRelatedField(
        queryset=Turno.objects.all(), source='turno', write_only=True, required=False
    )

    class Meta:
        model = InscripcionTurno
        fields = ("id", "turno", "turno_id", "voluntario", "voluntario_id", "estado", "fecha_inscripcion")
        read_only_fields = ("id", "fecha_inscripcion",)

    def validate(self, data):
        turno = data.get("turno")
        voluntario = data.get("voluntario")
        if turno is None or voluntario is None:
            return data

        # Check if voluntario has an active inscription to the voluntariado
        voluntariado = turno.voluntariado
        has_convocatoria_inscription = InscripcionConvocatoria.objects.filter(
            voluntariado=voluntariado,
            voluntario=voluntario,
            estado__in=[InscripcionConvocatoria.Status.INSCRITO, InscripcionConvocatoria.Status.ACEPTADO],
            is_active=True
        ).exists()
        
        if not has_convocatoria_inscription:
            raise serializers.ValidationError("Debes estar inscripto en el voluntariado antes de inscribirte a un turno.")

        # cupo actual (contar inscripciones activas)
        activos = turno.inscripciones.filter(estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO]).count()
        if activos >= turno.cupo:
            raise serializers.ValidationError("El turno ya está completo.")
        # unique_together ya evita duplicados en DB, pero chequeamos para dar mensaje claro
        if InscripcionTurno.objects.filter(turno=turno, voluntario=voluntario, estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO]).exists():
            raise serializers.ValidationError("Ya estás inscripto en este turno.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)
    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class InscripcionConvocatoriaSerializer(serializers.ModelSerializer):
    # Nested read fields
    voluntario = VoluntarioSerializer(read_only=True)
    voluntariado = VoluntariadoSerializer(read_only=True)
    
    # Write-only fields
    voluntario_id = serializers.PrimaryKeyRelatedField(
        queryset=Voluntario.objects.all(), source='voluntario', write_only=True, required=False
    )
    voluntariado_id = serializers.PrimaryKeyRelatedField(
        queryset=Voluntariado.objects.all(), source='voluntariado', write_only=True, required=False
    )

    class Meta:
        model = InscripcionConvocatoria
        fields = ("id", "voluntariado", "voluntariado_id", "voluntario", "voluntario_id", "estado", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, data):
        voluntariado = data.get("voluntariado")
        voluntario = data.get("voluntario")
        
        if voluntariado is None or voluntario is None:
            return data

        # Check if voluntariado is in "Convocatoria" stage
        today = timezone.now().date()
        
        if not voluntariado.fecha_inicio_convocatoria or not voluntariado.fecha_fin_convocatoria:
            raise serializers.ValidationError(
                "El voluntariado no tiene fechas de convocatoria configuradas."
            )
        
        # Check if we're in the convocatoria period
        if today < voluntariado.fecha_inicio_convocatoria:
            raise serializers.ValidationError(
                "La convocatoria para este voluntariado aún no ha comenzado."
            )
        
        if today > voluntariado.fecha_fin_convocatoria:
            raise serializers.ValidationError(
                "La convocatoria para este voluntariado ya ha finalizado."
            )

        # Check if voluntario is already inscribed (active inscription)
        if InscripcionConvocatoria.objects.filter(
            voluntariado=voluntariado, 
            voluntario=voluntario, 
            estado=InscripcionConvocatoria.Status.INSCRITO,
            is_active=True
        ).exists():
            raise serializers.ValidationError("Ya estás inscripto en este voluntariado.")
        
        return data

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)
    
    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

