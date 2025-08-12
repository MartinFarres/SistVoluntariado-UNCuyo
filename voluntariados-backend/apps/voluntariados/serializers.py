from rest_framework import serializers
from django.db import transaction
from .models import Voluntariado, Turno, InscripcionTurno
from voluntarios.models import Voluntario

class VoluntariadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntariado
        fields = ("id", "titulo", "descripcion", "organizacion", "facultad", "fecha_inicio", "fecha_fin", "estado", "creado_por", "created_at")
        read_only_fields = ("id", "creado_por", "created_at")

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
