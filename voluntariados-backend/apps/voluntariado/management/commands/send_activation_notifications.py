from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.voluntariado.models import Voluntariado
from apps.voluntariado.notifications import check_and_notify_activation


class Command(BaseCommand):
    help = "Envía correos de activación a los voluntarios aceptados de voluntariados que están activos y aún no fueron notificados."

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        # Buscar voluntariados candidatos: con fechas de cursado y sin marca de notificación
        qs = Voluntariado.objects.filter(
            fecha_inicio_cursado__isnull=False,
            fecha_fin_cursado__isnull=False,
            notificacion_activo_enviada_at__isnull=True,
        )
        total = 0
        enviados = 0
        for v in qs:
            total += 1
            enviados += check_and_notify_activation(v)
        self.stdout.write(self.style.SUCCESS(
            f"Procesados {total} voluntariados. Correos encolados: {enviados}."
        ))
