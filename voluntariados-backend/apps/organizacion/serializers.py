from rest_framework import serializers
from .models import Organizacion
from apps.ubicacion.models import Localidad
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class OrganizacionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Organizacion.

    Maneja la validación y la representación de datos para las organizaciones.
    - Para escritura (crear/actualizar), espera el ID de `localidad` opcionalmente.
    - Para lectura, provee datos anidados y detallados para `localidad`.
    """
    # Para escritura, esperamos un ID. `localidad` es opcional.
    localidad = serializers.PrimaryKeyRelatedField(
        queryset=Localidad.objects.all(), required=False, allow_null=True
    )
    # Image fields (will return URLs when present)
    logo = serializers.ImageField(required=False, allow_null=True, use_url=True)
    banner = serializers.ImageField(required=False, allow_null=True, use_url=True)
    # Optional public-facing fields
    slogan = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    url = serializers.URLField(required=False, allow_blank=True, allow_null=True)


    class Meta:
        model = Organizacion
        fields = (
            "id", "nombre", "descripcion", "activo",
            "contacto_email", "localidad", 
            "direccion", "logo", "banner", "slogan", "url"
        )
        # Campos que no se pueden editar a través del serializer.
        read_only_fields = ("id", )

        # Reglas de validación extra para los campos.
        extra_kwargs = {
            "nombre": {"required": True, "allow_blank": False},
            "descripcion": {"required": False, "allow_blank": True},
            "contacto_email": {"required": False, "allow_blank": True},
            "direccion": {"required": False, "allow_blank": True},
            "activo": {"required": False}
        }


    def validate_nombre(self, value):
        """Asegura que el nombre no esté compuesto solo de espacios."""
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_contacto_email(self, value):
        """Valida el formato del email de contacto."""
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Por favor, introduce una dirección de email válida.")
        return value
