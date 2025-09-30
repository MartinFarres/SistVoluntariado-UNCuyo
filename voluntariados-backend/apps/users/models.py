from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        """Crea y guarda un usuario común con email y password."""
        if not email:
            raise ValueError(gettext_lazy("El email es obligatorio"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Crea un superusuario con contraseña."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("El superusuario debe tener contraseña")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # importante: guardar contraseña
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMINISTRATIVO = "ADMIN", gettext_lazy("Administrativo")
        DELEGADO = "DELEG", gettext_lazy("Delegado")
        VOLUNTARIO = "VOL", gettext_lazy("Voluntario")

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.VOLUNTARIO,
    )
    persona = models.OneToOneField(
        "persona.Persona",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="user",
    )

    # Campos necesarios para AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def set_unusable_password(self):
        """Override for OAuth-only login."""
        super().set_unusable_password()
