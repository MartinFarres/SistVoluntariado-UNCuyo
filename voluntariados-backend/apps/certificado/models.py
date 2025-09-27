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

class Certificado(SoftDeleteModel):
    asistencia = models.ForeignKey(Asistencia, on_delete=models.SET_NULL, null=True,  related_name='asistencia')
    archivo = models.FileField(upload_to='certificado/%Y/%m/%d', null=True, blank=True)
    autoridades = models.ManyToManyField('Autoridad', related_name='certificados')
