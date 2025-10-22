from rest_framework import serializers
from django.db import transaction
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado
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

    descripcion = DescripcionVoluntariadoSerializer(read_only=True)
    gestionador = GestionadorSerializer(read_only=True, source='gestionadores')
    voluntarios_count = serializers.IntegerField(read_only=True, required=False)
    turnos_count = serializers.IntegerField(read_only=True, required=False)
    organizacion = OrganizacionSerializer(read_only=True)
    descripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=DescripcionVoluntariado.objects.all(), source='descripcion', write_only=True, required=False, allow_null=True
    )
    gestionadores_id = serializers.PrimaryKeyRelatedField(
        queryset=Gestionador.objects.all(), source='gestionadores', write_only=True, required=False, allow_null=True
    )
    organizacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Organizacion.objects.all(), source='organizacion', write_only=True, required=False, allow_null=True
    )


    class Meta:
        model = Voluntariado
        fields = (
            'id', 'nombre', 'estado', 'fecha_inicio', 'fecha_fin', 'organizacion',
            'descripcion',    # Campo de lectura (objeto anidado)
            'gestionador',    # Campo de lectura (objeto anidado)
            'voluntarios_count',  # Campo de lectura (anotación)
            'turnos_count',       # Campo de lectura (anotación)
            'descripcion_id', # Campo de escritura
            'gestionadores_id',  # Campo de escritura
            'organizacion_id'
        )

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate(self, data):
        """
        Check that fecha_fin is not earlier than fecha_inicio.
        """
        if data.get('fecha_inicio') and data.get('fecha_fin') and data['fecha_inicio'] > data['fecha_fin']:
            raise serializers.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
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

