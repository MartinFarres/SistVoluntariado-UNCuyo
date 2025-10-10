from rest_framework import serializers
from .models import Pais, Provincia, Departamento, Localidad

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = "__all__"

        extra_kwargs = {
            "nombre": {"required": True, "allow_null": False, "allow_blank": False},
        }

    def validate_nombre(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras")
        
        # Exclude current instance during updates
        queryset = Pais.objects.filter(nombre=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("Ya existe un país con este nombre.")
        
        return value

class ProvinciaSerializer(serializers.ModelSerializer):
    pais = PaisSerializer(read_only=True)
    pais_id = serializers.PrimaryKeyRelatedField(source="pais", queryset=Pais.objects.all(), write_only=True)

    class Meta:
        model = Provincia
        fields = "__all__"

        extra_kwargs = {
            "nombre": {"required": True, "allow_null": False, "allow_blank": False},
            "pais": {"required": True, "allow_null": False},
        }

    def validate_nombre(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras")

        # Exclude current instance during updates
        queryset = Provincia.objects.filter(nombre=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("Ya existe una provincia con este nombre.")

        return value

class DepartamentoSerializer(serializers.ModelSerializer):
    provincia = ProvinciaSerializer(read_only=True)
    provincia_id = serializers.PrimaryKeyRelatedField(source="provincia", queryset=Provincia.objects.all(), write_only=True)

    class Meta:
        model = Departamento
        fields = "__all__"
        read_only_fields = ("id",)

        extra_kwargs = {
            "nombre": {"required": True, "allow_null": False, "allow_blank": False},
            "provincia": {"required": True, "allow_null": False},
        }

    def validate_nombre(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras")
        
        # Exclude current instance during updates
        queryset = Departamento.objects.filter(nombre=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("Ya existe un departamento con este nombre.")
        
        return value

class LocalidadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer(read_only=True)
    departamento_id = serializers.PrimaryKeyRelatedField(source="departamento", queryset=Departamento.objects.all(), write_only=True)

    class Meta:
        model = Localidad
        fields = "__all__"
        read_only_fields = ("id",)

        extra_kwargs = {
            "nombre": {"required": True, "allow_null": False, "allow_blank": False},
            "departamento": {"required": True, "allow_null": False},
        }
        
    def validate_nombre(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("El nombre solo puede contener letras")

        # Exclude current instance during updates
        queryset = Localidad.objects.filter(nombre=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("Ya existe una localidad con este nombre.")

        return value