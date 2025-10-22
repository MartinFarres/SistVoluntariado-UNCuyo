from django.db import models
from django.conf import settings
import secrets

def generate_api_key():
    """Genera una clave de API segura."""
    return secrets.token_urlsafe(32)

class APIKey(models.Model):
    """
    Modelo para almacenar claves de API para acceso externo (ej. Power BI).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_key',
        verbose_name="Usuario"
    )
    key = models.CharField(
        max_length=64, 
        unique=True, 
        default=generate_api_key,
        editable=False,
        verbose_name="Clave de API"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último uso"
    )

    class Meta:
        verbose_name = "Clave de API"
        verbose_name_plural = "Claves de API"
        ordering = ['-created_at']

    def __str__(self):
        return f"Clave de API para {self.user.email}"
