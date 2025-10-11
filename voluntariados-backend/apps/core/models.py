from django.db import models
from django.core.validators import RegexValidator
from apps.soft_delete.model import SoftDeleteModel


class LandingConfig(SoftDeleteModel):
    """
    Modelo para almacenar la configuración global de la página de inicio.
    
    Este modelo permite configurar el contenido dinámico de la landing page,
    incluyendo información de contacto, redes sociales y textos principales.
    Solo debe existir una instancia de este modelo en la base de datos.
    """
    
    # Información básica del sitio
    page_title = models.CharField(
        max_length=100,
        verbose_name="Título de la página",
        help_text="Título que aparece en la pestaña del navegador",
        default="Sistema de Voluntariado"
    )
    
    site_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del sitio",
        help_text="Nombre principal del sitio web",
        default="Voluntariado UNCuyo"
    )
    
    # Imagen principal
    hero_image = models.FileField(
        upload_to='landing/hero/',
        verbose_name="Imagen principal",
        help_text="Archivo de imagen de fondo o principal de la landing page",
        null=True,
        blank=True
    )
    
    # Información de contacto
    contact_email = models.EmailField(
        verbose_name="Email de contacto",
        help_text="Dirección de email principal para contacto",
        null=True,
        blank=True
    )
    
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Número de teléfono",
        help_text="Número de teléfono de contacto",
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="El número de teléfono debe estar en formato válido (ej: +541234567890)"
            )
        ],
        null=True,
        blank=True
    )
    
    # Redes sociales
    instagram_handle = models.CharField(
        max_length=50,
        verbose_name="Instagram",
        help_text="Nombre de usuario de Instagram (sin @)",
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_.]+$',
                message="El handle de Instagram solo puede contener letras, números, puntos y guiones bajos"
            )
        ],
        null=True,
        blank=True
    )
    
    # Texto del footer
    footer_text = models.TextField(
        verbose_name="Texto del footer",
        help_text="Texto que aparece en el pie de página",
        default="© 2025 Universidad Nacional de Cuyo. Todos los derechos reservados.",
        null=True,
        blank=True
    )
    
    # Campos adicionales para mayor flexibilidad
    welcome_message = models.TextField(
        verbose_name="Mensaje de bienvenida",
        help_text="Mensaje principal de bienvenida en la landing page",
        default="Bienvenido al Sistema de Voluntariado",
        null=True,
        blank=True
    )
    
    description = models.TextField(
        verbose_name="Descripción del sitio",
        help_text="Descripción breve del sitio para SEO y presentación",
        null=True,
        blank=True
    )
    
    # Campos de auditoría heredados de SoftDeleteModel
    # created_at, updated_at, deleted_at
    
    class Meta:
        verbose_name = "Configuración de Landing"
        verbose_name_plural = "Configuración de Landing"
        db_table = "core_landing_config"
    
    def __str__(self):
        return f"Configuración Landing - {self.site_name}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para asegurar que solo exista una instancia.
        Si ya existe una configuración, actualiza la existente en lugar de crear una nueva.
        """
        if not self.pk and LandingConfig.objects.exists():
            # Si no tenemos pk (es nuevo) pero ya existe una configuración,
            # obtenemos la existente y la actualizamos
            existing = LandingConfig.objects.first()
            self.pk = existing.pk
        
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """
        Método de clase para obtener la configuración actual.
        Si no existe, crea una con valores por defecto.
        """
        config, created = cls.objects.get_or_create(
            pk=1,  # Siempre usamos el mismo ID
            defaults={
                'page_title': 'Sistema de Voluntariado',
                'site_name': 'Voluntariado UNCuyo',
                'welcome_message': 'Bienvenido al Sistema de Voluntariado',
                'footer_text': '© 2025 Universidad Nacional de Cuyo. Todos los derechos reservados.',
            }
        )
        return config