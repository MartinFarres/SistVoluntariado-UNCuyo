from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.users.permissions import IsAdministrador
from .models import LandingConfig
from .serializers import LandingConfigSerializer


class LandingConfigRetrieveView(generics.RetrieveAPIView):
    """
    Vista para obtener la configuración de la landing page.
    Acceso público para que el frontend pueda mostrar la información.
    """
    serializer_class = LandingConfigSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        """Siempre retorna la configuración actual."""
        return LandingConfig.get_config()


class LandingConfigUpdateView(generics.UpdateAPIView):
    """
    Vista para actualizar la configuración de la landing page.
    Requiere autenticación de administrador.
    """
    serializer_class = LandingConfigSerializer
    permission_classes = [IsAdministrador]
    
    def get_object(self):
        """Siempre retorna la configuración actual."""
        return LandingConfig.get_config()
    
    def put(self, request, *args, **kwargs):
        """Maneja la actualización completa de la configuración."""
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """Maneja la actualización parcial de la configuración."""
        return self.partial_update(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([AllowAny])
def landing_config_public(request):
    """
    Endpoint público simplificado para obtener solo los datos esenciales
    de la configuración de la landing page.
    """
    config = LandingConfig.get_config()
    
    # Datos mínimos para la landing page pública
    public_data = {
        'page_title': config.page_title,
        'site_name': config.site_name,
        'welcome_message': config.welcome_message,
        'description': config.description,
        'contact_email': config.contact_email,
        'phone_number': config.phone_number,
        'footer_text': config.footer_text,
    }
    
    # Agregar imagen si existe
    if config.hero_image:
        public_data['hero_image'] = request.build_absolute_uri(config.hero_image.url)
    
    # Agregar Instagram si existe
    if config.instagram_handle:
        public_data['instagram_handle'] = config.instagram_handle
        public_data['instagram_url'] = f"https://instagram.com/{config.instagram_handle}"

    # Campos dinámicos: listas JSON que vienen desde el backend
    # Añadimos tal cual, pero normalizamos imageUrl cuando sea relativo
    public_data['info_items'] = config.info_items or []
    public_data['how_it_works_steps'] = config.how_it_works_steps or []

    def _normalize_images(list_objs):
        res = []
        for it in (list_objs or []):
            if not isinstance(it, dict):
                res.append(it)
                continue
            img = it.get('imageUrl') or it.get('imageurl')
            if img:
                if isinstance(img, str) and img.startswith('/'):
                    it['imageUrl'] = request.build_absolute_uri(img)
                else:
                    it['imageUrl'] = img
            res.append(it)
        return res

    public_data['testimonials'] = _normalize_images(config.testimonials)
    public_data['team_members'] = _normalize_images(config.team_members)

    # About-related public fields
    public_data['mission'] = config.mission or ''
    public_data['vision'] = config.vision or ''
    public_data['offers_students'] = config.offers_students or []
    public_data['offers_organizations'] = config.offers_organizations or []

    # Some about-related lists may include image urls; normalize if present
    public_data['values'] = _normalize_images(config.values)
    public_data['stats'] = config.stats or []
    public_data['milestones'] = _normalize_images(config.milestones)
    
    return Response(public_data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAdministrador])
def landing_config_admin(request):
    """
    Endpoint para administradores que permite obtener y actualizar
    la configuración completa de la landing page.
    """
    config = LandingConfig.get_config()
    
    if request.method == 'GET':
        serializer = LandingConfigSerializer(config, context={'request': request})
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = LandingConfigSerializer(
            config, 
            data=request.data, 
            partial=partial,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def landing_stats_dynamic(request):
    """
    Endpoint público para obtener estadísticas dinámicas de la plataforma.
    Retorna conteos en tiempo real de voluntarios, organizaciones y voluntariados.
    También calcula las horas totales trabajadas sumando el base_horas configurado.
    Las etiquetas de las métricas son fijas y no se pueden cambiar, solo los números base.
    """
    from apps.persona.models import Voluntario
    from apps.organizacion.models import Organizacion
    from apps.voluntariado.models import Voluntariado
    from apps.asistencia.models import Asistencia
    from django.db.models import Sum
    
    # Get config for base numbers
    config = LandingConfig.get_config()
    base_voluntarios = int(config.base_voluntarios or 0)
    base_organizaciones = int(config.base_organizaciones or 0)
    base_proyectos = int(config.base_proyectos or 0)
    base_horas = float(config.base_horas or 0)
    
    # Count active records from database
    voluntarios_db = Voluntario.objects.filter(is_active=True).count()
    organizaciones_db = Organizacion.objects.filter(is_active=True, activo=True).count()
    
    # Count voluntariados by status
    from django.utils import timezone
    today = timezone.now().date()
    
    proyectos_db = Voluntariado.objects.filter(is_active=True).count()
    voluntariados_activos = Voluntariado.objects.filter(
        is_active=True,
        fecha_inicio_cursado__isnull=False,
        fecha_fin_cursado__isnull=False,
        fecha_inicio_cursado__lte=today,
        fecha_fin_cursado__gte=today
    ).count()
    
    # Calculate total hours from Asistencia records
    total_horas_result = Asistencia.objects.filter(
        is_active=True,
        presente=True,
        horas__isnull=False
    ).aggregate(total_horas=Sum('horas'))
    
    horas_db = float(total_horas_result.get('total_horas') or 0)
    
    # Calculate totals with base numbers
    voluntarios_total = voluntarios_db + base_voluntarios
    organizaciones_total = organizaciones_db + base_organizaciones
    proyectos_total = proyectos_db + base_proyectos
    horas_total = horas_db + base_horas
    
    return Response({
        # These are the fixed metrics that will always be displayed
        'voluntarios': voluntarios_total,
        'organizaciones': organizaciones_total,
        'proyectos': proyectos_total,
        'horas': round(horas_total, 2),
        
        # Breakdown for transparency (optional, for admin purposes)
        'voluntarios_db': voluntarios_db,
        'organizaciones_db': organizaciones_db,
        'proyectos_db': proyectos_db,
        'horas_db': round(horas_db, 2),
        'base_voluntarios': base_voluntarios,
        'base_organizaciones': base_organizaciones,
        'base_proyectos': base_proyectos,
        'base_horas': round(base_horas, 2),
        
        # Legacy fields for backward compatibility
        'voluntariados_total': proyectos_total,
        'voluntariados_activos': voluntariados_activos,
        'total_horas': round(horas_total, 2),
    })