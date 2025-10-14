from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Exponer campos públicos
        fields = ("id", "email", "role", "persona", "settled_up")
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

    class Meta:
        model = User
        fields = ("id", "email", "password", "role", "persona", "settled_up")
        read_only_fields = ("id", "persona", "settled_up")  # persona is auto-created, settled_up defaults to False

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
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
 