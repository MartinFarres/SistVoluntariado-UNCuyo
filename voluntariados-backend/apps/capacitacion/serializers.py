from rest_framework import serializers
from .models import Capacitacion, InscripcionCapacitacion
from apps.voluntariado.models import Voluntariado
from apps.capacitacion.models import Capacitacion
from apps.persona.models import Voluntario
from django.utils import timezone


class CapacitacionSerializer(serializers.ModelSerializer):
    voluntariado = serializers.PrimaryKeyRelatedField(
        queryset=Voluntariado.objects.all(),
        required=False,
        allow_null=True
    ) 
    
    class Meta:
        model = Capacitacion
        fields = (
            "id", "titulo", "descripcion", "fecha",
            "hora_inicio", "hora_fin", "cupo", "voluntariado",
        )
        read_only_fields = ("id",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # evitar import circular
        from apps.voluntariado.models import Voluntariado
        self.fields["voluntariado"].queryset = Voluntariado.objects.all()

    def validate(self, data):
        # validación de horario: si vienen horas, hora_inicio < hora_fin
        hi = data.get("hora_inicio") or getattr(self.instance, "hora_inicio", None)
        hf = data.get("hora_fin") or getattr(self.instance, "hora_fin", None)
        if hi and hf and hi >= hf:
            raise serializers.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        # la fecha no puede ser en el pasado (opcional)
        fecha = data.get("fecha") or getattr(self.instance, "fecha", None)
        if fecha and fecha < timezone.localdate():
            # permití si querés editar capacitaciones pasadas; aquí lo bloqueo
            raise serializers.ValidationError("La fecha de la capacitación no puede ser en el pasado.")
        # cupo si está presente debe ser positivo
        cupo = data.get("cupo") if "cupo" in data else getattr(self.instance, "cupo", None)
        if cupo is not None and cupo <= 0:
            raise serializers.ValidationError("El cupo debe ser un número positivo.")
        return data
    
    def create(self, validated_data):
        # creado_por lo establece la view
        return super().create(validated_data)   
    def update(self, instance, validated_data):
        # actualizado_por lo establece la view
        return super().update(instance, validated_data)
    

class InscripcionCapacitacionSerializer(serializers.ModelSerializer):
    capacitacion = serializers.PrimaryKeyRelatedField(queryset=Capacitacion.objects.all())
    voluntario = serializers.PrimaryKeyRelatedField(queryset=Voluntario.objects.all())

    class Meta:
        model = InscripcionCapacitacion
        fields = ("id", "capacitacion", "voluntario", "fecha_inscripcion", "aprobado")
        read_only_fields = ("id", "fecha_inscripcion")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.capacitacion.models import Capacitacion as CapModel
        self.fields["capacitacion"].queryset = CapModel.objects.all()
        self.fields["voluntario"].queryset = Voluntario.objects.all()

    def validate(self, data):
        capacitacion = data.get("capacitacion")
        voluntario = data.get("voluntario")
        if not capacitacion or not voluntario:
            return data

        # evitar duplicados (aunque model tiene unique_together)
        if InscripcionCapacitacion.objects.filter(capacitacion=capacitacion, voluntario=voluntario).exists():
            raise serializers.ValidationError("Ya estás inscripto en esta capacitación.")

        # validar cupo
        if capacitacion.cupo:
            inscritos = InscripcionCapacitacion.objects.filter(capacitacion=capacitacion).count()
            if inscritos >= capacitacion.cupo:
                raise serializers.ValidationError("La capacitación ya alcanzó su cupo máximo.")
        return data
