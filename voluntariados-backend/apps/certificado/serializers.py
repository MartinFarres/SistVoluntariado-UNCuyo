import os

from rest_framework import serializers
from .models import Certificado, Autoridad, EncabezadoCertificado


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


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if ext not in valid_extensions:
        raise serializers.ValidationError('Solo se permiten archivos PNG o JPG.')
    return value

class EncabezadoCertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncabezadoCertificado
        fields = ['id', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'actualizado']

    def validate_imagen_1(self, value):
        return validate_image_extension(value)

    def validate_imagen_2(self, value):
        return validate_image_extension(value)

    def validate_imagen_3(self, value):
        return validate_image_extension(value)

    def validate_imagen_4(self, value):
        return validate_image_extension(value)

class CertificadoSerializer(serializers.ModelSerializer):
    autoridades = AutoridadSerializer(many=True, read_only=True)
    autoridades_ids = serializers.PrimaryKeyRelatedField(
        queryset=Autoridad.objects.all(),
        many=True,
        write_only=True,
        source='autoridades'
    )

    class Meta:
        model = Certificado
        fields = ('id', 'asistencia', 'archivo', 'autoridades', 'autoridades_ids')

    def validate_asistencia(self, value):
        if value is None:
            raise serializers.ValidationError("El campo asistencia no puede ser nulo.")
        return value

    def validate_autoridades(self, value):
        if not value:
            raise serializers.ValidationError("Debe seleccionar al menos una autoridad.")
        return value
