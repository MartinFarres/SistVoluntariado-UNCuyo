from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    
    return Response(public_data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
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