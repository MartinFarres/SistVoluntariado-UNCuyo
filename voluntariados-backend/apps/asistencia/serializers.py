from rest_framework import serializers
from .models import Asistencia
from apps.voluntariado.models import InscripcionTurno

class AsistenciaSerializer(serializers.ModelSerializer):
    inscripcion = serializers.PrimaryKeyRelatedField(queryset=InscripcionTurno.objects.all())

    class Meta:
        model = Asistencia
        fields = ("id", "inscripcion", "presente", "horas", "observaciones")
        read_only_fields = ("id", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set queryset at runtime to avoid circular import issues
        if "inscripcion" in self.fields:
            self.fields["inscripcion"].queryset = __import__("apps.voluntariado.models", fromlist=["InscripcionTurno"]).InscripcionTurno.objects.all()

    def validate(self, data):
        """
        Validaciones básicas:
        - asegurarse que la inscripcion exista y que no exista otra asistencia (OneToOne en el modelo lo impide pero damos mensaje claro)
        """
        inscripcion = data.get("inscripcion")
        if not inscripcion:
            raise serializers.ValidationError("Se requiere inscripcion.")
        # si ya existe una asistencia y estamos creando
        if self.instance is None and hasattr(inscripcion, "asistencia"):
            raise serializers.ValidationError("Ya existe un registro de asistencia para esta inscripción.")
        return data

    def create(self, validated_data):
        # registrada_por la pone la view (si no, aquí podríamos usar context['request'].user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
