from rest_framework import serializers
from .models import Persona

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            "id", "nombre", "apellido", "dni", "fecha_nacimiento",
            "telefono", "email", "direccion", "localidad", "created_at", "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at")
    def validate_dni(self, value):
        if value <= 0:
            raise serializers.ValidationError("El DNI debe ser un número positivo.")
        return value
    def validate_telefono(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo números.")
        return value
    def validate_email(self, value):
        if value and "@" not in value:
            raise serializers.ValidationError("El email debe ser una dirección válida.")
        return value
    def validate_direccion(self, value):  
        if value and len(value) > 200:
            raise serializers.ValidationError("La dirección no puede exceder 200 caracteres.")
        return value
    def validate(self, data):
        # Validaciones cruzadas si es necesario
        return data
    def create(self, validated_data):
        return super().create(validated_data)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data) 