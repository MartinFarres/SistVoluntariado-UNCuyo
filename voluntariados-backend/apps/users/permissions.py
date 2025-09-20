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