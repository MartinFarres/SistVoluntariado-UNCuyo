from django.db import models

class Persona(models.Model):
    dni = models.CharField(max_length=20, unique=True)   # Documento, unique to avoid duplicates
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.dni})"
