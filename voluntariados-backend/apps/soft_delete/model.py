from django.db import models

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        # Borrado lógico: marcar como inactivo
        return super().update(is_active=False)

    def hard_delete(self):
        # Borrado real
        return super().delete()

    def alive(self):
        return self.filter(is_active=True)

    def dead(self):
        return self.filter(is_active=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Por defecto, devolver solo activos
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_only(self):
        return self.all_with_deleted().dead()


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    objects = SoftDeleteManager()        # Devuelve solo activos
    all_objects = SoftDeleteQuerySet.as_manager()  # Incluye todos

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # Borrado lógico
        self.is_active = False
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        # Borrado real
        super().delete(using=using, keep_parents=keep_parents)
