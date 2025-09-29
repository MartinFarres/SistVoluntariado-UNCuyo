
from rest_framework import serializers
from .models import Certificado, Autoridad

class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ('id', 'asistencia', 'archivo', 'autoridades')

    def validate_asistencia(self, value):

        if value is None:
            raise serializers.ValidationError("El campo asistencia no puede ser nulo.")
        return value

    def validate_autoridades(self, value):

        if not value:
            raise serializers.ValidationError("Debe seleccionar al menos una autoridad.")
        return value

class AutoridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autoridad
        fields = ('id', 'nombre', 'apellido', 'cargo', 'entidad_encargada', 'firma')

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_apellido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío.")
        return value

    def validate_cargo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El cargo no puede estar vacío.")
        return value
    
    def validate_entidad_encargada(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La entidad encargada no puede estar vacía.")
        return value
