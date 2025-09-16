from django.db import models
from apps.soft_delete.model import SoftDeleteModel


# Modelos básicos de ubicación geográfica: País, Provincia, Departamento, Localidad

class Pais(SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Provincia(SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="provincias")

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"

class Departamento(SoftDeleteModel):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, related_name="departamentos")

    def __str__(self):
        return f"{self.nombre} - {self.provincia.nombre}"

class Localidad(SoftDeleteModel):
    nombre = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name="localidades")
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.departamento.provincia.nombre})"
