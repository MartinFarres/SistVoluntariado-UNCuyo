import os
from django.db import models

from apps.asistencia.models import Asistencia
from apps.soft_delete.model import SoftDeleteModel

def authority_signature_path(instance, filename):
    nombre = instance.nombre
    apellido = instance.apellido
    cargo = instance.cargo
    _, extension = os.path.splitext(filename)
    return f'firmas/firma-{nombre}-{apellido}-{cargo}{extension}'

class Autoridad(SoftDeleteModel):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cargo = models.CharField(max_length=150)
    entidad_encargada = models.CharField(max_length=150)
    firma = models.FileField(upload_to=authority_signature_path, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"

class Certificado(SoftDeleteModel):
    asistencia = models.ForeignKey(Asistencia, on_delete=models.SET_NULL, null=True,  related_name='asistencia')
    archivo = models.FileField(upload_to='certificado/%Y/%m/%d', null=True, blank=True)
    autoridades = models.ManyToManyField('Autoridad', related_name='certificados')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if ext not in valid_extensions:
        raise ValueError('Solo se permiten archivos PNG o JPG.')

def encabezado_certificado_path(instance, filename):
    return f'certificados/encabezado/{filename}'

class EncabezadoCertificado(SoftDeleteModel):

    def encabezado_imagen_1_path(instance, filename):
        _, ext = os.path.splitext(filename)
        return f"encabezado/imagen-1{ext.lower()}"

    def encabezado_imagen_2_path(instance, filename):
        _, ext = os.path.splitext(filename)
        return f"encabezado/imagen-2{ext.lower()}"

    def encabezado_imagen_3_path(instance, filename):
        _, ext = os.path.splitext(filename)
        return f"encabezado/imagen-3{ext.lower()}"

    def encabezado_imagen_4_path(instance, filename):
        _, ext = os.path.splitext(filename)
        return f"encabezado/imagen-4{ext.lower()}"

    imagen_1 = models.FileField(upload_to=encabezado_imagen_1_path, blank=True, null=True)
    imagen_2 = models.FileField(upload_to=encabezado_imagen_2_path, blank=True, null=True)
    imagen_3 = models.FileField(upload_to=encabezado_imagen_3_path, blank=True, null=True)
    imagen_4 = models.FileField(upload_to=encabezado_imagen_4_path, blank=True, null=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Encabezado de certificado"
        verbose_name_plural = "Encabezados de certificados"

    def __str__(self):
        return f"Encabezado {self.id} - {self.actualizado.strftime('%d/%m/%Y')}"

