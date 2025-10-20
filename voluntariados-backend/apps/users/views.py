from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .serializers import UserCreateSerializer
from rest_framework import permissions
from .permissions import IsAdministrador

User = get_user_model()

class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("persona")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current authenticated user
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def setup_persona(self, request):
        """
        Complete persona setup for the authenticated user
        """
        user = request.user
        
        if user.settled_up:
            return Response(
                {"detail": "User persona setup already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Import here to avoid circular imports
        from apps.persona.models import Voluntario, Administrativo, Delegado
        from apps.persona.serializers import VoluntarioSerializer, AdministrativoSerializer, DelegadoSerializer
        
        # Update the existing persona instance for the user
        persona_data = request.data.copy()
        
        if not user.persona:
            return Response({"detail": "No persona instance found for user"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the specific persona subclass instance based on user role
        try:
            if user.role == user.Roles.VOLUNTARIO:
                persona_instance = Voluntario.objects.get(pk=user.persona.pk)
                serializer = VoluntarioSerializer(persona_instance, data=persona_data, partial=True)
            elif user.role == user.Roles.ADMINISTRATIVO:
                persona_instance = Administrativo.objects.get(pk=user.persona.pk)
                serializer = AdministrativoSerializer(persona_instance, data=persona_data, partial=True)
            elif user.role == user.Roles.DELEGADO:
                persona_instance = Delegado.objects.get(pk=user.persona.pk)
                serializer = DelegadoSerializer(persona_instance, data=persona_data, partial=True)
            else:
                return Response({"detail": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)
        except (Voluntario.DoesNotExist, Administrativo.DoesNotExist, Delegado.DoesNotExist):
            return Response({"detail": "Persona instance not found"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            user.settled_up = True
            user.save()
            return Response({
                "detail": "Persona setup updated successfully",
                "persona": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # usamos distintos serializers para list/create
    def get_serializer_class(self):
        if self.action in ("create",):
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsAdministrador()]
        if self.action == "list":
            return [IsAdministrador()]
        if self.action == "create":
            return [permissions.AllowAny()]
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
        if user.role == user.Roles.ADMINISTRATIVO or user.is_staff:
            return User.objects.all().select_related("persona")
        return User.objects.filter(id=user.id).select_related("persona")