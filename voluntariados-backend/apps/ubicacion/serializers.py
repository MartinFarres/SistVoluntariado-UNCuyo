from rest_framework import serializers
from .models import Pais, Provincia, Departamento, Localidad

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ("id", "nombre", "codigo")

class ProvinciaSerializer(serializers.ModelSerializer):
    pais = PaisSerializer(read_only=True)
    pais_id = serializers.PrimaryKeyRelatedField(source="pais", queryset=Pais.objects.all(), write_only=True)

    class Meta:
        model = Provincia
        fields = ("id", "nombre", "pais", "pais_id")

class DepartamentoSerializer(serializers.ModelSerializer):
    provincia = ProvinciaSerializer(read_only=True)
    provincia_id = serializers.PrimaryKeyRelatedField(source="provincia", queryset=Provincia.objects.all(), write_only=True)

    class Meta:
        model = Departamento
        fields = ("id", "nombre", "provincia", "provincia_id")


class LocalidadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer(read_only=True)
    departamento_id = serializers.PrimaryKeyRelatedField(source="departamento", queryset=Departamento.objects.all(), write_only=True)

    class Meta:
        model = Localidad
        fields = ("id", "nombre", "departamento", "departamento_id", "codigo_postal")
        read_only_fields = ("id",)
    
    