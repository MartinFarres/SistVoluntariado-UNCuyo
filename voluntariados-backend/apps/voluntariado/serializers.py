from rest_framework import serializers
from django.db import transaction
from .models import Voluntariado, Turno, InscripcionTurno, DescripcionVoluntariado
from apps.persona.models import Voluntario, Gestionador

class VoluntariadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntariado
        fields = ('id', 'nombre', 'turno', 'descripcion', 'fecha_inicio', 'fecha_fin', 'Gestionadores', 'estado')

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
    
    def validate_turno(self, value):
        if value is None:
            raise serializers.ValidationError("El turno no puede ser nulo.")
        return value

    def validate_descripcion(self, value):
        if value is None:
            raise serializers.ValidationError("La descripción no puede ser nula.")
        return value

    def validate_Gestionadores(self, value):
        if value is None:
            raise serializers.ValidationError("Debe asignar al menos un gestionador.")
        return value

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ("id", "voluntariado", "fecha", "hora_inicio", "hora_fin", "cupo", "lugar", "created_at")
        read_only_fields = ("id", "created_at")

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
