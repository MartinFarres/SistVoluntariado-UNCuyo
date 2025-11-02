import datetime
from typing import Optional

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from apps.voluntariado.models import InscripcionTurno


class Command(BaseCommand):
    help = "Send reminder emails to volunteers one day before their scheduled shift (Turno)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            help=(
                "Optional ISO date (YYYY-MM-DD) to use as 'today' for calculating reminders. "
                "Useful for testing. If omitted, uses current date in timezone.now()."
            ),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only print what would be sent without sending any emails.",
        )
        parser.add_argument(
            "--force-send",
            action="store_true",
            help=(
                "When used together with --dry-run, actually send emails even if settings.DEBUG is False. "
                "Use with caution in production."
            ),
        )

    def handle(self, *args, **options):
        today_override = options.get("date")
        dry_run = options.get("dry_run", False)

        if today_override:
            try:
                today = datetime.date.fromisoformat(today_override)
            except ValueError:
                self.stderr.write(self.style.ERROR("--date must be in YYYY-MM-DD format"))
                return
        else:
            today = timezone.now().date()

        tomorrow = today + datetime.timedelta(days=1)
        self.stdout.write(
            self.style.NOTICE(f"Preparing shift reminders for date: {tomorrow.isoformat()}")
        )

        qs = (
            InscripcionTurno.objects.filter(
                turno__fecha=tomorrow,
                estado__in=[
                    InscripcionTurno.Status.INSCRITO,
                    InscripcionTurno.Status.ASISTIO,
                ],
            )
            .select_related(
                "turno",
                "turno__voluntariado",
                "voluntario__persona_ptr__user",
            )
            .order_by("turno__hora_inicio", "voluntario__apellido", "voluntario__nombre")
        )

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No shift enrollments found for tomorrow."))
            return

        sent = 0
        skipped = 0

        for ins in qs:
            # Resolve recipient email from linked user
            email = self._get_email_for_inscripcion(ins)
            if not email:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping inscripcion id={ins.id}: no email for volunteer"
                    )
                )
                continue

            turno = ins.turno
            voluntariado = turno.voluntariado
            voluntariado_nombre = voluntariado.nombre if voluntariado else 'Voluntariado'
            voluntariado_id = voluntariado.id if voluntariado else None

            subject = f"⏰ Recordatorio de turno - {voluntariado_nombre}"
            
            fecha_fmt = turno.fecha.strftime("%d/%m/%Y")
            hora_inicio_fmt = turno.hora_inicio.strftime("%H:%M")
            hora_fin_fmt = turno.hora_fin.strftime("%H:%M")
            lugar = turno.lugar or "(a confirmar)"

            # Build direct link to voluntariado details
            frontend_url = getattr(settings, 'FRONTEND_URL', None)
            voluntariado_link = ""
            if frontend_url and voluntariado_id:
                voluntariado_link = f"{frontend_url}/voluntariados/{voluntariado_id}"

            # Plain text version
            text_body_parts = [
                "=" * 60,
                "⏰ RECORDATORIO DE TURNO",
                "=" * 60,
                "",
                "Hola,",
                "",
                "Este es un recordatorio de tu turno de voluntariado para mañana.",
                "",
                "📋 DETALLES DEL TURNO:",
                f"   Programa: {voluntariado_nombre}",
                f"   📅 Fecha: {fecha_fmt}",
                f"   🕐 Horario: {hora_inicio_fmt} - {hora_fin_fmt}",
                f"   📍 Lugar: {lugar}",
                "",
                "⚠️ IMPORTANTE:",
                "• Por favor, llegá unos minutos antes del horario de inicio.",
                "• Si no podés asistir, avisá a la coordinación lo antes posible.",
                "",
            ]
            
            if voluntariado_link:
                text_body_parts.extend([
                    f"🔗 Ver detalles del voluntariado: {voluntariado_link}",
                    "",
                ])
            
            text_body_parts.extend([
                "¡Gracias por tu compromiso y participación!",
                "",
                "Saludos cordiales,",
                "Sistema de Voluntariado",
                "Universidad Nacional de Cuyo",
                "",
                "=" * 60,
            ])
            
            text_body = "\n".join(text_body_parts)

            # HTML version with professional styling (matching convocatoria acceptance email)
            button_html = ""
            if voluntariado_link:
                button_html = f"""
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{voluntariado_link}" 
                           style="background-color: #007bff; color: white; padding: 14px 28px; 
                                  text-decoration: none; border-radius: 6px; font-weight: bold; 
                                  display: inline-block; font-size: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            📋 Ver Detalles del Voluntariado
                        </a>
                    </div>
                """
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
                    <tr>
                        <td align="center">
                            <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden;">
                                <!-- Header -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                                        <h1 style="color: white; margin: 0; font-size: 28px; font-weight: bold;">
                                            ⏰ Recordatorio de Turno
                                        </h1>
                                    </td>
                                </tr>
                                
                                <!-- Reminder Badge -->
                                <tr>
                                    <td align="center" style="padding: 30px 30px 10px;">
                                        <div style="background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 50px; 
                                                    display: inline-block; padding: 10px 25px;">
                                            <span style="color: #856404; font-weight: bold; font-size: 16px;">
                                                📅 Turno Mañana
                                            </span>
                                        </div>
                                    </td>
                                </tr>
                                
                                <!-- Main Content -->
                                <tr>
                                    <td style="padding: 20px 40px;">
                                        <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                                            Hola,
                                        </p>
                                        <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 25px;">
                                            Este es un recordatorio de tu turno de voluntariado para <strong>mañana</strong>.
                                        </p>
                                        
                                        <!-- Shift Details Box -->
                                        <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 25px; margin: 25px 0; border-radius: 4px;">
                                            <h3 style="color: #667eea; margin: 0 0 15px; font-size: 18px;">
                                                📋 Detalles del Turno
                                            </h3>
                                            <table width="100%" cellpadding="8" cellspacing="0">
                                                <tr>
                                                    <td style="color: #666; font-size: 15px; padding: 8px 0;">
                                                        <strong style="color: #333;">Programa:</strong>
                                                    </td>
                                                    <td style="color: #555; font-size: 15px; padding: 8px 0;">
                                                        {voluntariado_nombre}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #666; font-size: 15px; padding: 8px 0;">
                                                        <strong style="color: #333;">📅 Fecha:</strong>
                                                    </td>
                                                    <td style="color: #555; font-size: 15px; padding: 8px 0;">
                                                        {fecha_fmt}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #666; font-size: 15px; padding: 8px 0;">
                                                        <strong style="color: #333;">🕐 Horario:</strong>
                                                    </td>
                                                    <td style="color: #555; font-size: 15px; padding: 8px 0;">
                                                        {hora_inicio_fmt} - {hora_fin_fmt}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="color: #666; font-size: 15px; padding: 8px 0;">
                                                        <strong style="color: #333;">📍 Lugar:</strong>
                                                    </td>
                                                    <td style="color: #555; font-size: 15px; padding: 8px 0;">
                                                        {lugar}
                                                    </td>
                                                </tr>
                                            </table>
                                        </div>
                                        
                                        <!-- Important Notes Box -->
                                        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin: 25px 0; border-radius: 4px;">
                                            <h3 style="color: #856404; margin: 0 0 10px; font-size: 18px;">
                                                ⚠️ Importante
                                            </h3>
                                            <ul style="color: #856404; margin: 0; padding-left: 20px; font-size: 15px; line-height: 1.8;">
                                                <li>Por favor, <strong>llegá unos minutos antes</strong> del horario de inicio.</li>
                                                <li>Si no podés asistir, <strong>avisá a la coordinación</strong> lo antes posible.</li>
                                            </ul>
                                        </div>
                                        
                                        {button_html}
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="background-color: #f8f9fa; padding: 30px 40px; border-top: 1px solid #e0e0e0;">
                                        <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0 0 15px;">
                                            ¡Gracias por tu compromiso y participación!
                                        </p>
                                        <p style="color: #666; font-size: 14px; margin: 0;">
                                            <strong>Sistema de Voluntariado</strong><br>
                                            Universidad Nacional de Cuyo
                                        </p>
                                    </td>
                                </tr>
                                
                                <!-- Bottom Bar -->
                                <tr>
                                    <td style="background-color: #333; padding: 15px; text-align: center;">
                                        <p style="color: #999; font-size: 12px; margin: 0;">
                                            © 2025 Universidad Nacional de Cuyo - Sistema de Voluntariado
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """

            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@example.com"

            if dry_run:
                # In DEBUG mode, performing a dry-run will actually send the email so
                # developers can inspect the rendered message (console backend or SMTP).
                # In non-DEBUG (production), dry-run only simulates unless --force-send is used.
                will_send = getattr(settings, 'DEBUG', False) or options.get('force_send')

                if will_send:
                    try:
                        send_mail(
                            subject=subject,
                            message=text_body,
                            from_email=from_email,
                            recipient_list=[email],
                            fail_silently=False,
                            html_message=html_body,
                        )
                        sent += 1
                        note = "[DRY RUN - SENT]" if getattr(settings, 'DEBUG', False) and not options.get('force_send') else "[DRY RUN - FORCED SEND]"
                        self.stdout.write(self.style.NOTICE(f"{note} Sent to {email}: {subject} | {fecha_fmt} {hora_inicio_fmt} @ {lugar}"))
                    except Exception as exc:
                        skipped += 1
                        self.stderr.write(self.style.ERROR(f"Failed to send to {email} (inscripcion id={ins.id}): {exc}"))
                else:
                    # Not sending in production without explicit --force-send
                    self.stdout.write(self.style.NOTICE(
                        f"[DRY RUN] Would send to {email}: {subject} | {fecha_fmt} {hora_inicio_fmt} @ {lugar} (use --force-send to actually send)"
                    ))
                continue

            try:
                send_mail(
                    subject=subject,
                    message=text_body,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                    html_message=html_body,
                )
                sent += 1
                self.stdout.write(self.style.SUCCESS(f"Sent reminder to {email}"))
            except Exception as exc:
                skipped += 1
                self.stderr.write(
                    self.style.ERROR(f"Failed to send to {email} (inscripcion id={ins.id}): {exc}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Reminders processed: {total}. Sent: {sent}. Skipped: {skipped}."
            )
        )

    def _get_email_for_inscripcion(self, inscripcion) -> Optional[str]:
        """Return the volunteer email if available, else None.

        Access pattern follows multi-table inheritance: Voluntario -> Persona -> User
        as configured in the project models.
        """
        try:
            # Prefer resolving through persona_ptr to ensure select_related is used
            user = getattr(inscripcion.voluntario.persona_ptr, "user", None)
            if user and user.email:
                return user.email
        except Exception:
            pass

        # Fallback: try direct attribute in case inheritance descriptor resolves it
        try:
            user = getattr(inscripcion.voluntario, "user", None)
            if user and user.email:
                return user.email
        except Exception:
            pass

        return None
