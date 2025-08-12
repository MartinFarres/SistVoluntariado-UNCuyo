from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMINISTRATIVO = "ADMIN", _("Administrativo")
        DELEGADO = "DELEG", _("Delegado")
        VOLUNTARIO = "VOL", _("Voluntario")

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.VOLUNTARIO)
    persona = models.OneToOneField(
        "personas.Persona", null=True, blank=True, on_delete=models.SET_NULL, related_name="user"
    )

    REQUIRED_FIELDS = ["email"]
    # Usar email como username:
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
