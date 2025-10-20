from rest_framework import permissions

class IsAdministrador(permissions.BasePermission):
    """
    Permite la acción solo si el usuario es de tipo ADMINISTRATIVO
    """

    def has_permission(self, request, view):
        # request.user es tu modelo User custom
        if request.user.is_authenticated:
            return request.user.role == request.user.Roles.ADMINISTRATIVO
        return False


class IsVoluntario(permissions.BasePermission):
    """
    Permite la acción solo si el usuario es de tipo Voluntario
    """

    def has_permission(self, request, view):
        # request.user es tu modelo User custom
        if request.user.is_authenticated:
            return request.user.role == request.user.Roles.VOLUNTARIO
        return False
    

class IsDelegado(permissions.BasePermission):
    """
    Permite la acción solo si el usuario es de tipo DELEGADO
    """

    def has_permission(self, request, view):
        # request.user es tu modelo User custom
        if request.user.is_authenticated:
            return request.user.role == request.user.Roles.DELEGADO
        return False


class CanUpdateOwnPersona(permissions.BasePermission):
    """
    Permite que los usuarios actualicen su propia persona o que los administradores actualicen cualquier persona.
    Previene que los usuarios eliminen su propia persona (solo admins pueden eliminar).
    """

    def has_permission(self, request, view):
        # Permitir acceso si está autenticado
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Administradores tienen acceso completo
        if request.user.role == request.user.Roles.ADMINISTRATIVO:
            return True
        
        # Para operaciones DELETE, solo administradores
        if request.method == 'DELETE':
            return False
        
        # Para GET, PATCH, PUT: los usuarios pueden acceder a su propia persona
        if hasattr(request.user, 'persona') and request.user.persona:
            return obj.id == request.user.persona.id
        
        return False

