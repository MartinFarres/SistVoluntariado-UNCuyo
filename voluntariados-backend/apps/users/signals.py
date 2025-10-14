from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.persona.models import Voluntario, Administrativo, Delegado
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def create_persona_for_user(sender, instance, created, **kwargs):
    """
    Automatically create the appropriate Persona when a User is created.
    """
    if created and not instance.persona:
        persona = None
        
        try:
            if instance.role == User.Roles.VOLUNTARIO:
                persona = Voluntario.objects.create(
                    nombre="",  # Will be filled in later by the user
                    apellido="",
                    email=instance.email,
                )
            elif instance.role == User.Roles.ADMINISTRATIVO:
                persona = Administrativo.objects.create(
                    nombre="",
                    apellido="",
                    email=instance.email,
                )
            elif instance.role == User.Roles.DELEGADO:
                persona = Delegado.objects.create(
                    nombre="",
                    apellido="",
                    email=instance.email,
                )
            
            if persona:
                instance.persona = persona
                # Use update to avoid triggering the signal again
                User.objects.filter(pk=instance.pk).update(persona=persona)
                logger.info(f"Created {persona.__class__.__name__} for user {instance.email}")
        
        except Exception as e:
            logger.error(f"Error creating persona for user {instance.email}: {str(e)}")
            # Don't re-raise to avoid breaking user creation