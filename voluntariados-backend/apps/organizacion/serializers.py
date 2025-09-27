from rest_framework import serializers
from .models import Organizacion
from apps.persona.models import Persona
from apps.ubicacion.models import Localidad
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class OrganizacionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Organizacion.

    Maneja la validación y la representación de datos para las organizaciones.
    - Para escritura (crear/actualizar), espera el ID de `localidad` y opcionalmente de `contacto_persona`.
    - Para lectura, provee datos anidados y detallados para `localidad` y `contacto_persona`.
    """
    # Para escritura, esperamos un ID. `localidad` es obligatoria.
    contacto_persona = serializers.PrimaryKeyRelatedField(
        queryset=Persona.objects.all(), required=False, allow_null=True
    )
    localidad = serializers.PrimaryKeyRelatedField(
        queryset=Localidad.objects.all(), required=True
    )

    # Para lectura, proveemos datos anidados de solo lectura para mayor contexto.
    contacto_persona_data = serializers.SerializerMethodField(read_only=True)
    localidad_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organizacion
        fields = (
            "id", "nombre", "descripcion", "activa",
            "contacto_email", "contacto_persona", "contacto_persona_data",
            "localidad", "localidad_data", "direccion",
            "created_at"
        )
        # Campos que no se pueden editar a través del serializer.
        read_only_fields = ("id", "created_at", "contacto_persona_data", "localidad_data", "activa")

        # Reglas de validación extra para los campos.
        extra_kwargs = {
            "nombre": {"required": True, "allow_blank": False},
            "descripcion": {"required": True, "allow_blank": False},
            "contacto_email": {"allow_blank": False},
            "direccion": {"required": True, "allow_blank": False},
        }

    def get_contacto_persona_data(self, obj):
        """Devuelve un diccionario con datos clave de la persona de contacto."""
        persona = getattr(obj, "contacto_persona", None)
        if not persona:
            return None
        return {
            "id": persona.id,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "email": persona.email,
            "telefono": persona.telefono,
        }

    def get_localidad_data(self, obj):
        """Devuelve un diccionario con datos clave de la ubicación."""
        loc = getattr(obj, "localidad", None)
        if not loc:
            return None
        return {
            "id": loc.id,
            "nombre": loc.nombre,
            "departamento": getattr(loc.departamento, "nombre", None),
            "provincia": getattr(getattr(loc.departamento, "provincia", None), "nombre", None),
        }

    def validate_nombre(self, value):
        """Asegura que el nombre no esté compuesto solo de espacios."""
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_contacto_email(self, value):
        """Valida el formato del email de contacto."""
        if value:
            try:
                validate_email(value)
            except ValidationError:
                raise serializers.ValidationError("Por favor, introduce una dirección de email válida.")
        return value

    def validate(self, data):
        """
        Valida a nivel de objeto: asegura que exista al menos un método de contacto.
        """
        if not data.get("contacto_email") and not data.get("contacto_persona"):
            raise serializers.ValidationError(
                "Debe proporcionar al menos un email de contacto o una persona de contacto."
            )
        return data

    def create(self, validated_data):
        # La lógica para 'creado_por' se puede manejar en la vista, usando request.user.
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # La lógica para 'actualizado_por' se puede manejar en la vista.
        return super().update(instance, validated_data)
