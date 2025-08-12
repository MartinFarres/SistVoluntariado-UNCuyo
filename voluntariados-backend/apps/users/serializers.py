from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Exponer campos públicos
        fields = ("id", "username", "email", "first_name", "last_name", "role", "persona")
        read_only_fields = ("id",)

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role", "persona")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
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
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value    
