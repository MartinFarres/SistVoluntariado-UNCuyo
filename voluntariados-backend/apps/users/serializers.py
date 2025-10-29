from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Exponer campos públicos
        fields = ("id", "email", "role", "persona", "settled_up", "signup_date", "last_login")
        read_only_fields = ("id", "role")  # Make role read-only for updates

    def validate(self, attrs):
        """Ensure role cannot be changed in updates."""
        if self.instance and 'role' in attrs:
            if self.instance.role != attrs['role']:
                raise serializers.ValidationError({
                    'role': gettext_lazy('El rol no puede ser modificado después de la creación del usuario.')
                })
        return attrs

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # Optional helper to set a Delegado's organizacion at creation time
    delegado_organizacion = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "role", "persona", "settled_up", "delegado_organizacion")
        read_only_fields = ("id", "persona", "settled_up")  # persona is auto-created, settled_up defaults to False

    def validate(self, attrs):
        """
        Ensure that if role is DELEG, delegado_organizacion is present and valid.
        """
        role = attrs.get('role')
        delegado_org = attrs.get('delegado_organizacion')
        if role == User.Roles.DELEGADO:
            if not delegado_org:
                raise serializers.ValidationError({'delegado_organizacion': gettext_lazy('Se requiere una organización para el rol Delegado.')})
            # verify organization exists
            try:
                from apps.organizacion.models import Organizacion
                if not Organizacion.objects.filter(pk=delegado_org).exists():
                    raise serializers.ValidationError({'delegado_organizacion': gettext_lazy('Organización inválida.')})
            except ImportError:
                # If import fails, skip validation (shouldn't happen in normal app)
                pass

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        # pop delegado_organizacion if present so it's not passed to User model
        delegado_org = validated_data.pop("delegado_organizacion", None)

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # If a delegado organization id was provided, try to assign it to the created persona
        if delegado_org and user.role == User.Roles.DELEGADO:
            try:
                # Import here to avoid circular imports
                from apps.organizacion.models import Organizacion
                persona = getattr(user, 'persona', None)
                if persona:
                    try:
                        org = Organizacion.objects.get(pk=delegado_org)
                        # Delegado persona has `organizacion` FK
                        persona.organizacion = org
                        persona.save()
                    except Organizacion.DoesNotExist:
                        # Ignore if org not found
                        pass
                else:
                    # If for some reason persona wasn't created by signal, create a Delegado and assign
                    from apps.persona.models import Delegado
                    d = Delegado.objects.create(nombre="", apellido="", organizacion_id=delegado_org)
                    user.persona = d
                    user.save()
            except Exception:
                # Don't break user creation if something goes wrong
                pass

        return user
    
    def update(self, instance, validated_data):
        # Remove role from validated_data to prevent any attempts to change it
        validated_data.pop('role', None)
        
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting a password reset."""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate email exists (but don't reveal if it doesn't for security)."""
        # We validate but don't raise error to prevent email enumeration
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset with token."""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """Validate that both passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Las contraseñas no coinciden.'
            })
        return attrs
 