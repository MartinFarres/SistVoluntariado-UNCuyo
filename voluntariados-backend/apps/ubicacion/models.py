from django.db import models

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="provincias")

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, related_name="departamentos")

    def __str__(self):
        return f"{self.nombre} - {self.provincia.nombre}"

class Localidad(models.Model):
    nombre = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name="localidades")
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.departamento.provincia.nombre})"
