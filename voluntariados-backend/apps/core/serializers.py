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
            # Campos dinámicos de la landing
                "info_items", "testimonials", "how_it_works_steps", "team_members",
                # About-related fields
                "mission", "vision", "offers_students", "offers_organizations",
                "values", "stats", "milestones",
                # Base numbers for fixed metrics
                "base_voluntarios", "base_organizaciones", "base_proyectos", "base_horas",
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
            "info_items": {"required": False},
            "testimonials": {"required": False},
            "how_it_works_steps": {"required": False},
            "team_members": {"required": False},
            # About-related
            "mission": {"required": False},
            "vision": {"required": False},
            "offers_students": {"required": False},
            "offers_organizations": {"required": False},
            "values": {"required": False},
            "stats": {"required": False},
            "milestones": {"required": False},
            "base_voluntarios": {"required": False},
            "base_organizaciones": {"required": False},
            "base_proyectos": {"required": False},
            "base_horas": {"required": False},
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
        
        # Normalizar URLs de imágenes en listas JSON (si existen)
        request = self.context.get('request')
        for list_field in ('testimonials', 'team_members'):
            items = data.get(list_field)
            if items and isinstance(items, list):
                normalized = []
                for item in items:
                    if not isinstance(item, dict):
                        normalized.append(item)
                        continue
                    img = item.get('imageUrl') or item.get('imageurl')
                    if img and request:
                        # Si es ruta relativa, convertir a URL absoluta
                        if isinstance(img, str) and img.startswith('/'):
                            item['imageUrl'] = request.build_absolute_uri(img)
                        else:
                            # dejar tal cual si ya es absoluta o no inicia con /
                            item['imageUrl'] = img
                    normalized.append(item)
                data[list_field] = normalized
        
        return data