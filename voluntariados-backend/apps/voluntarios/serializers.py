from rest_framework import serializers
from apps.personas.models import Persona
from .models import Voluntario

class VoluntarioSerializer(serializers.ModelSerializer):
    persona = serializers.PrimaryKeyRelatedField(read_only=True)
    # Inicializamos con .none() para evitar la AssertionError de DRF
    persona_id = serializers.PrimaryKeyRelatedField(
        source="persona",
        queryset=Persona.objects.none(),  
        write_only=True
    )

    class Meta:
        model = Voluntario
        fields = (
            "id", "persona", "persona_id", "fecha_alta", "interno",
            "observaciones", "carrera", "activo",
        )
        read_only_fields = ("id", "fecha_alta")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Seteamos el queryset real en runtime para evitar import-cycles en nivel módulo
        self.fields["persona_id"].queryset = Persona.objects.all()
    def validate_carrera(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError("La carrera no puede exceder 100 caracteres.")
        return value
    
    def validate_observaciones(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Las observaciones no pueden exceder 500 caracteres.")
        return value    
    
    def validate(self, data):
        # Validaciones cruzadas si es necesario
        return data 
    
    def create(self, validated_data):
        return super().create(validated_data)   
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data) 
    
    