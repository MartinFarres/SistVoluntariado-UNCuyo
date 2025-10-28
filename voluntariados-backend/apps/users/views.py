from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from rest_framework import permissions
from .permissions import IsAdministrador
from .models import PasswordResetToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError

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

    @action(detail=False, methods=['post', 'put'], permission_classes=[IsAuthenticated])
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

        # For PUT (partial updates) allow clients to send only the fields they want
        # and avoid serializer errors for fields intentionally omitted or set to null.
        # Remove keys whose values are None or empty string so the serializer won't
        # validate them as required on partial updates.
        if request.method == 'PUT':
            persona_data = {k: v for k, v in persona_data.items() if v is not None and v != ''}
        
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
            try:
                serializer.save()
            except IntegrityError as e:
                # Return a user-friendly 400 instead of a 500 for integrity errors (e.g., duplicate DNI)
                errors = {"detail": "Error de integridad al actualizar la persona."}
                # If DNI was part of the payload, surface a clearer field error
                if 'dni' in persona_data:
                    errors = {"dni": ["Este DNI ya está registrado en el sistema."]}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            user.settled_up = True
            user.save()
            return Response({
                "detail": "Persona setup updated successfully",
                "persona": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset_request(self, request):
        """
        Request a password reset. Sends email with reset link.
        Always returns success to prevent email enumeration.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                
                # Invalidate any existing unused tokens for this email
                PasswordResetToken.objects.filter(email=email, used=False).update(used=True)
                
                # Create new reset token
                reset_token = PasswordResetToken.objects.create(email=email)
                
                # Build reset link
                frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
                reset_link = f"{frontend_url}/reset-password/{reset_token.token}"
                
                # Send email
                try:
                    send_mail(
                        subject='Restablecer Contraseña - Sistema de Voluntariado',
                        message=f'''
Hola,

Has solicitado restablecer tu contraseña en el Sistema de Voluntariado.

Haz clic en el siguiente enlace para restablecer tu contraseña:
{reset_link}

Este enlace expirará en 1 hora.

Si no solicitaste este cambio, puedes ignorar este correo.

Saludos,
Equipo de Voluntariado UNCuyo
                        ''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")
                    # Log but don't reveal to user
                    
            except User.DoesNotExist:
                # Don't reveal that user doesn't exist
                pass
            
            # Always return success to prevent email enumeration
            return Response({
                "detail": "Si el email existe en nuestro sistema, recibirás un correo con instrucciones para restablecer tu contraseña."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset_confirm(self, request):
        """
        Confirm password reset with token and set new password.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                reset_token = PasswordResetToken.objects.get(token=token)
                
                # Validate token
                if not reset_token.is_valid():
                    if reset_token.used:
                        return Response({
                            "detail": "Este enlace ya fue utilizado."
                        }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            "detail": "Este enlace ha expirado. Solicita un nuevo enlace de restablecimiento."
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                # Get user and update password
                try:
                    user = User.objects.get(email=reset_token.email)
                    user.set_password(new_password)
                    user.save()
                    
                    # Mark token as used
                    reset_token.used = True
                    reset_token.save()
                    
                    return Response({
                        "detail": "Contraseña restablecida exitosamente. Ya puedes iniciar sesión."
                    }, status=status.HTTP_200_OK)
                    
                except User.DoesNotExist:
                    return Response({
                        "detail": "Usuario no encontrado."
                    }, status=status.HTTP_404_NOT_FOUND)
                    
            except PasswordResetToken.DoesNotExist:
                return Response({
                    "detail": "Token inválido."
                }, status=status.HTTP_400_BAD_REQUEST)
        
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