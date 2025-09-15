from rest_framework import serializers
from .models import Persona, Voluntario
import re
from datetime import date

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"

        # Todos los campos son requeridos y no pueden ser nulos
        extra_kwargs = {
            "nombre": {"required": True, "allow_null": False, "allow_blank": False},
            "apellido": {"required": True, "allow_null": False, "allow_blank": False},
            "dni": {"required": True, "allow_null": False, "allow_blank": False},
            "fecha_nacimiento": {"required": True, "allow_null": False},
            "telefono": {"required": True, "allow_null": False, "allow_blank": False},
            "email": {"required": True, "allow_null": False, "allow_blank": False},
            "direccion": {"required": True, "allow_null": False, "allow_blank": False},
            "localidad": {"required": True, "allow_null": False},
        }

    def validate_nombre(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras.")
        return value

    def validate_apellido(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("El apellido solo puede contener letras.")
        return value

    def validate_dni(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("El DNI solo puede contener números.")
        return value

    def validate_fecha_nacimiento(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return value

    def validate_telefono(self, value):
        if value and not re.match(r"^\+?\d{7,15}$", value):
            raise serializers.ValidationError("El teléfono debe contener entre 7 y 15 dígitos (puede incluir +).")
        return value


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
    