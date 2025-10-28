from rest_framework import serializers
from .models import Persona, Voluntario, Gestionador, Administrativo, Delegado
import re
from datetime import date

class PersonaSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    
    class Meta:
        model = Persona
        fields = ['id', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'telefono', 
                  'direccion', 'localidad', 'is_active', 'email']

        # All the fields are required, and can't be null neither blank
        extra_kwargs = {
            "nombre": {"required": True, "allow_null": False, "allow_blank": False},
            "apellido": {"required": True, "allow_null": False, "allow_blank": False},
            "dni": {"required": True, "allow_null": False, "allow_blank": False},
            "fecha_nacimiento": {"required": True, "allow_null": False},
            "telefono": {"required": True, "allow_null": False, "allow_blank": False},
            "direccion": {"required": True, "allow_null": False, "allow_blank": False},
            "localidad": {"required": True, "allow_null": False},
        }
        read_only_fields = ("id", "email", "is_active")
    
    def get_email(self, obj):
        """Get email from related User if exists, otherwise return empty string"""
        try:
            # Use the related_name 'user' from User model
            if hasattr(obj, 'user') and obj.user:
                return obj.user.email
            return ""
        except Exception:
            return ""
        

    def validate_nombre(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras")
        return value

    def validate_apellido(self, value):
        if not value.replace(" ", "").isalpha():
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
        # Expose 'interno' so frontend can toggle it
        fields = (
            PersonaSerializer.Meta.fields
            + ['interno', 'carrera', 'observaciones', 'condicion', 'cantidad_observaciones_asistencia']
        )
        read_only_fields = PersonaSerializer.Meta.read_only_fields + ('cantidad_observaciones_asistencia',)

        # Takes the extra args from the parent and adds it's own
        # Important: carrera/condicion may be omitted or null on regular updates
        # (e.g., when switching to voluntario externo). Setup-time requirements are
        # enforced in the user setup endpoint.
        extra_kwargs = PersonaSerializer.Meta.extra_kwargs | {
            "carrera": {"required": False, "allow_null": True},
            "condicion": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def validate_observaciones(self, value):
        if value and len(value) > 512:
            raise serializers.ValidationError("Las observaciones no pueden exceder 512 caracteres.")
        return value

    def validate_condicion(self, value):
        # Allow empty/omitted condicion when switching to externo via partial update
        if value in (None, ""):
            return value
        allowed = [choice[0] for choice in self.Meta.model.Condicion.choices]
        if value not in allowed:
            raise serializers.ValidationError(f"Condición debe ser una de: {', '.join(allowed)}")
        return value

    def update(self, instance, validated_data):
        # If client explicitly sets interno to False, clear academic fields
        interno = validated_data.get('interno', instance.interno)
        if interno is False:
            # Carrera is nullable in model; removing it reflects 'externo' state
            validated_data['carrera'] = None
            # Set condicion to EXTERNO explicitly when switching to externo
            validated_data['condicion'] = self.Meta.model.Condicion.EXTERNO
        return super().update(instance, validated_data)
    


class GestionadorSerializer(PersonaSerializer):
    class Meta(PersonaSerializer.Meta):
        model = Gestionador
        fields = PersonaSerializer.Meta.fields
        extra_kwargs = PersonaSerializer.Meta.extra_kwargs


class AdministrativoSerializer(GestionadorSerializer):
    class Meta(GestionadorSerializer.Meta):
        model = Administrativo
        fields = GestionadorSerializer.Meta.fields
        extra_kwargs = GestionadorSerializer.Meta.extra_kwargs


class DelegadoSerializer(GestionadorSerializer):
    class Meta(GestionadorSerializer.Meta):
        model = Delegado
        fields = GestionadorSerializer.Meta.fields + ['organizacion']

        # Takes the extra args from the parent and adds it's own
        # organizacion is required during setup
        extra_kwargs = GestionadorSerializer.Meta.extra_kwargs | {
            "organizacion": {"required": True, "allow_null": False}
        }