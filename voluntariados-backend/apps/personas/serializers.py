from rest_framework import serializers
from .models import Persona
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
