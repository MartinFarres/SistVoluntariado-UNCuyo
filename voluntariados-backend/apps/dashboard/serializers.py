from rest_framework import serializers
from apps.persona.models import Voluntario
from apps.facultad.models import Carrera, Facultad
from .models import APIKey


class APIKeySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo APIKey. Expone la clave solo en la creación/lectura.
    """
    class Meta:
        model = APIKey
        fields = ['key', 'created_at']
        read_only_fields = ['key', 'created_at']


class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = ['nombre']


class CarreraSerializer(serializers.ModelSerializer):
    facultad = FacultadSerializer(read_only=True)

    class Meta:
        model = Carrera
        fields = ['nombre', 'facultad']


class VoluntarioPowerBISerializer(serializers.ModelSerializer):
    """
    Serializador detallado para exportar todos los datos de un voluntario a Power BI.
    Hereda campos del modelo Persona.
    """
    # Campos del modelo Persona (padre)
    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    dni = serializers.CharField(read_only=True)
    fecha_nacimiento = serializers.DateField(read_only=True)
    telefono = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    direccion = serializers.CharField(read_only=True)
    localidad_nombre = serializers.CharField(source='localidad.nombre', read_only=True, default=None)
    provincia_nombre = serializers.CharField(source='localidad.departamento.provincia.nombre', read_only=True, default=None)

    # Campos del modelo Voluntario
    carrera = CarreraSerializer(read_only=True)

    class Meta:
        model = Voluntario
        fields = [
            'id',
            'nombre',
            'apellido',
            'dni',
            'fecha_nacimiento',
            'telefono',
            'email',
            'direccion',
            'localidad_nombre',
            'provincia_nombre',
            'interno', # Campo específico de Voluntario
            'observaciones', # Campo específico de Voluntario
            'carrera',
        ]
