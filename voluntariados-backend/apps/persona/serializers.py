from rest_framework import serializers
from .models import Persona, Voluntario, Gestionador, Administrativo, Delegado
import re
from datetime import date

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"

        # All the fields are required, and can't be null neither blank
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
        read_only_fields = ("id", )
        

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



class VoluntarioSerializer(PersonaSerializer):
    """
    Voluntario serializer inherits from PersonaSerializer to get all it's validations
    and add more validations specific to the Voluntario model.
    """
    class Meta(PersonaSerializer.Meta):
        model = Voluntario
        fields = "__all__"

        # Takes the extra args from the parent and adds it's own
        extra_kwargs = PersonaSerializer.Meta.extra_kwargs | {
            "carrera": {"required": True, "allow_null": False},
        }

    def validate_observaciones(self, value):
        if value and len(value) > 512:
            raise serializers.ValidationError("Las observaciones no pueden exceder 512 caracteres.")
        return value
    


class GestionadorSerializer(PersonaSerializer):
    class Meta(PersonaSerializer.Meta):
        model = Gestionador
        fields = "__all__"
        extra_kwargs = PersonaSerializer.Meta.extra_kwargs


class AdministrativoSerializer(GestionadorSerializer):
    class Meta(GestionadorSerializer.Meta):
        model = Administrativo
        fields = "__all__"
        extra_kwargs = GestionadorSerializer.Meta.extra_kwargs


class DelegadoSerializer(GestionadorSerializer):
    class Meta(GestionadorSerializer.Meta):
        model = Delegado
        fields = "__all__"

        # Takes the extra args from the parent and adds it's own
        extra_kwargs = GestionadorSerializer.Meta.extra_kwargs | {
            "organizacion": {"required": True, "allow_null": False}
        }