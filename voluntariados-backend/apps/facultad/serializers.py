from rest_framework import serializers
from .models import Facultad, Carrera

class CarreraSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Carrera.
    - Para escritura, espera el ID de `facultad`.
    - Para lectura, provee datos anidados de la facultad.
    """
    facultad = serializers.PrimaryKeyRelatedField(
        queryset=Facultad.objects.all(), required=True
    )
    facultad_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Carrera
        fields = ("id", "nombre", "facultad", "facultad_data")
        read_only_fields = ("id", "facultad_data")
        extra_kwargs = {
            "nombre": {"required": True, "allow_blank": False},
        }

    def get_facultad_data(self, obj):
        """Devuelve un diccionario con datos clave de la facultad."""
        if obj.facultad:
            return {
                "id": obj.facultad.id,
                "nombre": obj.facultad.nombre,
            }
        return None

    def validate_nombre(self, value):
        """Asegura que el nombre de la carrera no esté vacío."""
        if not value.strip():
            raise serializers.ValidationError("El nombre de la carrera no puede estar vacío.")
        return value

class FacultadSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Facultad.
    Para lectura, incluye los nombres de las carreras asociadas.
    """
    # Usamos StringRelatedField para una representación simple y eficiente de las carreras,
    # que mostrará el resultado del método __str__ del modelo Carrera.
    carreras = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Facultad
        fields = ("id", "nombre", "descripcion", "fecha_creacion", "activa", "carreras")
        read_only_fields = ("id", "carreras", "fecha_creacion", "activa")
        extra_kwargs = {
            "nombre": {"required": True, "allow_blank": False},
            "descripcion": {"required": False, "allow_blank": True, "allow_null": True},
        }

    def validate_nombre(self, value):
        """Asegura que el nombre no esté vacío y no exceda la longitud."""
        if not value.strip():
            raise serializers.ValidationError("El nombre de la facultad no puede estar vacío.")
        # La validación de longitud máxima la hace el Model Field, pero esto da un error más amigable.
        if len(value) > 100:
            raise serializers.ValidationError("El nombre de la facultad no puede exceder 100 caracteres.")
        return value
