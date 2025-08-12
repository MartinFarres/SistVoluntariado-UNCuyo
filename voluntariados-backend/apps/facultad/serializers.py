from rest_framework import serializers
from .models import Facultad, Carrera

class CarreraSerializer(serializers.ModelSerializer):
    facultad = serializers.PrimaryKeyRelatedField(queryset=None, required=False, allow_null=True)

    class Meta:
        model = Carrera
        fields = ("id", "nombre", "facultad")
        read_only_fields = ("id",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # evitar import circular
        from apps.facultad.models import Facultad as FacModel
        self.fields["facultad"].queryset = FacModel.objects.all()

class FacultadSerializer(serializers.ModelSerializer):
    # opcional: listar carreras anidadas en lectura
    carreras = CarreraSerializer(many=True, read_only=True)

    class Meta:
        model = Facultad
        fields = ("id", "nombre", "descripcion", "fecha_creacion", "activa", "carreras")
        read_only_fields = ("id", "carreras")
    def validate_nombre(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("El nombre de la facultad no puede exceder 100 caracteres.")
        return value
    def validate(self, data):
        # validaciones adicionales si es necesario
        return data
    def create(self, validated_data):
        # creado_por lo establece la view
        return super().create(validated_data)
    def update(self, instance, validated_data):
        # actualizado_por lo establece la view
        return super().update(instance, validated_data)
    