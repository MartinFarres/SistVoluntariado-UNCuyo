from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("persona")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # usamos distintos serializers para list/create
    def get_serializer_class(self):
        if self.action in ("create",):
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsAdminOrSelf()]
        if self.action == "list":
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save()  # no seteamos creado_por, lo maneja el serializer

    
    def perform_update(self, serializer):
        serializer.save()  # no seteamos modificado_por, lo maneja el serializer

    def perform_destroy(self, instance):
        instance.delete()  # no seteamos modificado_por, lo maneja el modelo
    
    def get_queryset(self):
        # Admins ven todos, usuarios normales solo a ellos mismos
        user = self.request.user
        if user.is_staff:
            return User.objects.all().select_related("persona")
        return User.objects.filter(id=user.id).select_related("persona")