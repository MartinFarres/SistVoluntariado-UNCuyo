from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import LandingConfig


@admin.register(LandingConfig)
class LandingConfigAdmin(admin.ModelAdmin):
    """
    Configuración del admin para LandingConfig.
    
    Permite gestionar fácilmente la configuración de la landing page
    desde el panel de administración de Django.
    """
    
    list_display = ('site_name', 'page_title', 'contact_email', 'has_hero_image')
    search_fields = ('site_name', 'page_title', 'contact_email')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('page_title', 'site_name', 'welcome_message', 'description')
        }),
        ('Imagen Principal', {
            'fields': ('hero_image', 'hero_image_preview'),
            'description': 'Archivo de imagen principal que aparece en la landing page'
        }),
        ('Información de Contacto', {
            'fields': ('contact_email', 'phone_number'),
            'classes': ('collapse',)
        }),
        ('Redes Sociales', {
            'fields': ('instagram_handle',),
            'classes': ('collapse',)
        }),
        ('Pie de Página', {
            'fields': ('footer_text',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('hero_image_preview', )
    
    def has_add_permission(self, request):
        """
        Evita crear múltiples configuraciones.
        Solo permite editar la existente.
        """
        return not LandingConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """
        No permite eliminar la configuración.
        """
        return False
    
    def has_hero_image(self, obj):
        """Indica si tiene imagen principal."""
        return bool(obj.hero_image)
    has_hero_image.boolean = True
    has_hero_image.short_description = 'Tiene imagen'
    
    def hero_image_preview(self, obj):
        """Muestra una vista previa de la imagen principal."""
        if obj.hero_image:
            return mark_safe(
                f'<img src="{obj.hero_image.url}" style="max-height: 200px; max-width: 300px;" />'
            )
        return "No hay imagen"
    hero_image_preview.short_description = 'Vista previa'
    
    def get_queryset(self, request):
        """
        Asegura que siempre exista una configuración.
        """
        qs = super().get_queryset(request)
        if not qs.exists():
            LandingConfig.get_config()  # Crea la configuración por defecto
        return qs
    
    def changelist_view(self, request, extra_context=None):
        """
        Personaliza la vista de lista para mostrar solo una configuración.
        """
        # Si existe configuración, redirige directamente a editarla
        if LandingConfig.objects.exists():
            config = LandingConfig.objects.first()
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(
                reverse('admin:core_landingconfig_change', args=[config.pk])
            )
        
        return super().changelist_view(request, extra_context)
    
    def save_model(self, request, obj, form, change):
        """
        Asegura que solo exista una configuración.
        """
        if not change and LandingConfig.objects.exists():
            # Si está creando y ya existe una, actualiza la existente
            existing = LandingConfig.objects.first()
            for field in form.cleaned_data:
                setattr(existing, field, form.cleaned_data[field])
            existing.save()
        else:
            super().save_model(request, obj, form, change)