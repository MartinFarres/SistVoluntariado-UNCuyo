from rest_framework import serializers
from .models import Pais, Provincia, Departamento, Localidad

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = "__all__"

class ProvinciaSerializer(serializers.ModelSerializer):
    pais = PaisSerializer(read_only=True)
    pais_id = serializers.PrimaryKeyRelatedField(source="pais", queryset=Pais.objects.all(), write_only=True)

    class Meta:
        model = Provincia
        fields = "__all__"

class DepartamentoSerializer(serializers.ModelSerializer):
    provincia = ProvinciaSerializer(read_only=True)
    provincia_id = serializers.PrimaryKeyRelatedField(source="provincia", queryset=Provincia.objects.all(), write_only=True)

    class Meta:
        model = Departamento
        fields = "__all__"
        read_only_fields = ("id",)

class LocalidadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer(read_only=True)
    departamento_id = serializers.PrimaryKeyRelatedField(source="departamento", queryset=Departamento.objects.all(), write_only=True)

    class Meta:
        model = Localidad
        fields = "__all__"
        read_only_fields = ("id",)
    
    