from rest_framework import serializers
from .models import LandingConfig


class LandingConfigSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo LandingConfig.
    
    Maneja la configuración global de la landing page,
    incluyendo validaciones para campos específicos.
    """
    
    class Meta:
        model = LandingConfig
        fields = (
            "id", "page_title", "site_name", "hero_image",
            "contact_email", "phone_number", "instagram_handle",
            "footer_text", "welcome_message", "description",
        )
        read_only_fields = ("id", )
        
        extra_kwargs = {
            "page_title": {"required": False},
            "site_name": {"required": False},
            "hero_image": {"required": False},
            "contact_email": {"required": False},
            "phone_number": {"required": False},
            "instagram_handle": {"required": False},
            "footer_text": {"required": False},
            "welcome_message": {"required": False},
            "description": {"required": False},
        }
    
    def validate_instagram_handle(self, value):
        """Valida que el handle de Instagram no incluya el símbolo @."""
        if value and value.startswith('@'):
            raise serializers.ValidationError(
                "No incluyas el símbolo '@' en el handle de Instagram."
            )
        return value
    
    def validate_hero_image(self, value):
        """Valida que el archivo sea una imagen válida."""
        if value:
            # Verificar que tenga una extensión de imagen válida
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
            if hasattr(value, 'name') and value.name:
                if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                    raise serializers.ValidationError(
                        "El archivo debe ser una imagen válida (.jpg, .jpeg, .png, .gif, .webp, .svg)."
                    )
            # Verificar el tamaño del archivo (opcional, por ejemplo 10MB)
            if hasattr(value, 'size') and value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    "El archivo no puede ser mayor a 10MB."
                )
        return value
    
    def validate_phone_number(self, value):
        """Validación adicional para el número de teléfono."""
        if value:
            # Remover espacios y caracteres especiales comunes
            cleaned = value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not cleaned.replace('+', '').isdigit():
                raise serializers.ValidationError(
                    "El número de teléfono solo debe contener dígitos, espacios, guiones y paréntesis."
                )
        return value
    
    def to_representation(self, instance):
        """Personaliza la representación de salida."""
        data = super().to_representation(instance)
        
        # Agregar URL completa para el archivo si existe
        if data.get('hero_image'):
            request = self.context.get('request')
            if request:
                data['hero_image'] = request.build_absolute_uri(data['hero_image'])
        
        # Agregar URL de Instagram si existe
        if data.get('instagram_handle'):
            data['instagram_url'] = f"https://instagram.com/{data['instagram_handle']}"
        
        return data