from rest_framework import serializers
from django.db import transaction
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado
from apps.persona.models import Voluntario, Gestionador
from ..persona.serializers import GestionadorSerializer


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
    class Meta:
        model = Turno
        fields = ("id", "fecha", "hora_inicio", "hora_fin", "cupo", "lugar","voluntariado","voluntariado_id",)
        read_only_fields = ("id",)

class VoluntariadoSerializer(serializers.ModelSerializer):
    # --- Campos para Lectura ---

    descripcion = DescripcionVoluntariadoSerializer(read_only=True)
    gestionador = GestionadorSerializer(read_only=True, source='gestionadores')
    descripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=DescripcionVoluntariado.objects.all(), source='descripcion', write_only=True, required=False, allow_null=True
    )
    gestionador_id = serializers.PrimaryKeyRelatedField(
        queryset=Gestionador.objects.all(), source='gestionadores', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Voluntariado
        fields = (
            'id', 'nombre', 'estado', 'fecha_inicio', 'fecha_fin', 'organizacion',
            'descripcion',    # Campo de lectura (objeto anidado)
            'gestionador',    # Campo de lectura (objeto anidado)
            'descripcion_id', # Campo de escritura
            'gestionador_id'  # Campo de escritura
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

class InscripcionTurnoSerializer(serializers.ModelSerializer):
    # Exponer algunos campos anidados si se quiere
    class Meta:
        model = InscripcionTurno
        fields = ("id", "turno", "voluntario", "estado", "fecha_inscripcion")
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
        if InscripcionTurno.objects.filter(turno=turno, voluntario=voluntario).exists():
            raise serializers.ValidationError("Ya estás inscripto en este turno.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)
    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
