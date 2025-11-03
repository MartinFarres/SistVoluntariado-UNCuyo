from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from apps.voluntariado.models import Turno, InscripcionTurno
from django.conf import settings


class Command(BaseCommand):
    help = "Send reminder emails to volunteers one day before their scheduled shift (Turno)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            default=None,
            help="Treat this date (YYYY-MM-DD) as 'today' for the command.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be sent without dispatching emails.",
        )
        parser.add_argument(
            "--force-send",
            action="store_true",
            help="Ignore any de-duplication logic and force sending (no-op by default).",
        )

    def handle(self, *args, **options):
        # Determine the working date
        date_str = options.get("date")
        dry_run = options.get("dry_run", False)
        _force = options.get("force_send", False)

        if date_str:
            try:
                today = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                self.stderr.write(self.style.ERROR("Invalid --date format. Use YYYY-MM-DD"))
                return
        else:
            today = timezone.localdate()

        target = today + timedelta(days=1)

        # Find tomorrow's shifts
        turnos = Turno.objects.filter(is_active=True, fecha=target)
        total_emails = 0

        for turno in turnos:
            # Notify volunteers with active inscription on this shift
            inscripciones = InscripcionTurno.objects.select_related("voluntario__user").filter(
                turno=turno,
                is_active=True,
                estado__in=[InscripcionTurno.Status.INSCRITO, InscripcionTurno.Status.ASISTIO],
            )

            for ins in inscripciones:
                user = getattr(ins.voluntario, "user", None)
                email = getattr(user, "email", None) if user else None
                if not email:
                    continue

                subject = "Recordatorio de turno"
                text_body = (
                    f"Hola,\n\n"
                    f"Te recordamos que tenés un turno del voluntariado \"{turno.voluntariado}\" "
                    f"el día {turno.fecha} de {turno.hora_inicio} a {turno.hora_fin}.\n\n"
                    f"¡Gracias por participar!"
                )

                if dry_run:
                    self.stdout.write(f"[DRY-RUN] Would send reminder to {email} for turno {turno.id} on {turno.fecha}")
                else:
                    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or None
                    try:
                        send_mail(
                            subject=subject,
                            message=text_body,
                            from_email=from_email,
                            recipient_list=[email],
                            fail_silently=True,
                        )
                        total_emails += 1
                    except Exception:
                        # Do not break the loop due to a single failure
                        pass

        if dry_run:
            self.stdout.write(self.style.SUCCESS("[DRY-RUN] Completed send_shift_reminders."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Sent {total_emails} reminder email(s)."))
