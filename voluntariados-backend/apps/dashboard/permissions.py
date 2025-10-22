from rest_framework import permissions
from .models import APIKey
from django.utils import timezone

class HasAPIKey(permissions.BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a través de una clave de API válida.
    La clave debe ser enviada en el encabezado 'X-API-Key'.
    """
    def has_permission(self, request, view):
        # Permitir acceso si es un usuario autenticado y administrador (para la vista de gestión de claves)
        # o si la solicitud tiene una clave de API válida.
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True

        api_key_header = request.META.get('HTTP_X_API_KEY')
        if not api_key_header:
            return False

        try:
            api_key_obj = APIKey.objects.get(key=api_key_header)
            # Opcional: Actualizar la fecha de último uso
            api_key_obj.last_used_at = timezone.now()
            api_key_obj.save()
            # Asignar el usuario de la clave a request.user para que los logs lo registren
            request.user = api_key_obj.user
            return True
        except APIKey.DoesNotExist:
            return False
