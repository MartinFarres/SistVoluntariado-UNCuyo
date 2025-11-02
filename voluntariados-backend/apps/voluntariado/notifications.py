from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
import threading
from typing import Iterable

from .models import Voluntariado, InscripcionConvocatoria


def _build_activation_email(voluntariado: Voluntariado, turnos_link: str | None):
    nombre = getattr(voluntariado, 'nombre', 'un voluntariado')
    subject = f"🟢 Voluntariado activo - {nombre}"

    text_lines = [
        "=" * 60,
        "¡Felicitaciones!",
        "=" * 60,
        "",
        "✅ Inscripción Aceptada",
        "",
        "Hola,",
        "",
        f'Tu postulación al voluntariado "{nombre}" ha sido aceptada.',
        "",
        "📅 Próximo Paso",
        "",
        "Ya podés inscribirte a los turnos disponibles para este voluntariado.",
        "Elegí los horarios que mejor se adapten a tu disponibilidad.",
        "",
    ]
    if turnos_link:
        text_lines += [
            "Ver Turnos Disponibles:",
            f"{turnos_link}",
            "",
        ]
    text_lines += [
        "Muchas gracias por tu compromiso y participación.",
        "",
        "Sistema de Voluntariado",
        "Universidad Nacional de Cuyo",
        "",
        "© 2025 Universidad Nacional de Cuyo - Sistema de Voluntariado",
        "=" * 60,
    ]
    text_body = "\n".join(text_lines)

    button_html = ""
    if turnos_link:
        button_html = f"""
            <div style="text-align: center; margin: 30px 0;">
                <a href="{turnos_link}" 
                   style="background-color: #007bff; color: white; padding: 14px 28px; 
                          text-decoration: none; border-radius: 6px; font-weight: bold; 
                          display: inline-block; font-size: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    📅 Ver Turnos Disponibles
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
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 40px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden;">
                        <!-- Header with gradient -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">🎉</div>
                                <h1 style="color: white; margin: 0; font-size: 32px; font-weight: bold; letter-spacing: -0.5px;">
                                    ¡Felicitaciones!
                                </h1>
                            </td>
                        </tr>
                        
                        <!-- Success Badge -->
                        <tr>
                            <td align="center" style="padding: 30px 30px 20px;">
                                <div style="background-color: #d4edda; border: 2px solid #28a745; border-radius: 50px; 
                                            display: inline-block; padding: 12px 28px;">
                                    <span style="color: #155724; font-weight: 600; font-size: 16px;">
                                        ✅ Inscripción Aceptada
                                    </span>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Main Content -->
                        <tr>
                            <td style="padding: 0 40px 30px;">
                                <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                                    Hola,
                                </p>
                                <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                                    Tu postulación al voluntariado <strong style="color: #667eea;">"{nombre}"</strong> ha sido <strong>aceptada</strong>.
                                </p>
                                
                                <!-- Next Step Box -->
                                <div style="background: linear-gradient(135deg, #e8f4fd 0%, #f0e7ff 100%); border-left: 4px solid #667eea; padding: 24px; margin: 25px 0; border-radius: 8px;">
                                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                                        <span style="font-size: 24px; margin-right: 12px;">📅</span>
                                        <h3 style="color: #667eea; margin: 0; font-size: 18px; font-weight: 600;">
                                            Próximo Paso
                                        </h3>
                                    </div>
                                    <p style="color: #555; margin: 0; font-size: 15px; line-height: 1.6;">
                                        Ya podés inscribirte a los <strong>turnos disponibles</strong> para este voluntariado.
                                        Elegí los horarios que mejor se adapten a tu disponibilidad.
                                    </p>
                                </div>
                                
                                {button_html}
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 30px 40px; border-top: 1px solid #e0e0e0;">
                                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0 0 15px;">
                                    Muchas gracias por tu compromiso y participación.
                                </p>
                                <p style="color: #666; font-size: 14px; margin: 0; font-weight: 600;">
                                    Sistema de Voluntariado
                                </p>
                                <p style="color: #999; font-size: 13px; margin: 5px 0 0;">
                                    Universidad Nacional de Cuyo
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Bottom Bar -->
                        <tr>
                            <td style="background-color: #333; padding: 20px; text-align: center;">
                                <p style="color: #999; font-size: 12px; margin: 0; line-height: 1.4;">
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
    return subject, text_body, html_body


def notify_voluntariado_activated(voluntariado: Voluntariado) -> int:
    """
    Envía correos a todas las personas con InscripcionConvocatoria en estado ACEPTADO
    para el voluntariado dado. Devuelve la cantidad de correos encolados.
    Marca la notificación como enviada en el voluntariado para evitar duplicados.
    """
    frontend_url = getattr(settings, 'FRONTEND_URL', None)
    link = None
    if frontend_url:
        link = f"{frontend_url}/voluntariados/{voluntariado.id}#turnos-section"

    subject, text_body, html_body = _build_activation_email(voluntariado, link)
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or None

    # Obtener destinatarios (emails de usuarios aceptados)
    qs = InscripcionConvocatoria.objects.select_related('voluntario__user').filter(
        voluntariado=voluntariado,
        estado=InscripcionConvocatoria.Status.ACEPTADO,
        is_active=True,
    )
    recipients: list[str] = []
    for ic in qs:
        user = getattr(ic.voluntario, 'user', None)
        email = getattr(user, 'email', None) if user else None
        if email:
            recipients.append(email)

    if not recipients:
        # Marca igualmente para evitar intentos repetidos
        Voluntariado.objects.filter(pk=voluntariado.pk, notificacion_activo_enviada_at__isnull=True).update(
            notificacion_activo_enviada_at=timezone.now()
        )
        return 0

    def _send_all():
        try:
            for to in recipients:
                try:
                    send_mail(
                        subject=subject,
                        message=text_body,
                        from_email=from_email,
                        recipient_list=[to],
                        fail_silently=True,
                        html_message=html_body,
                    )
                except Exception:
                    # no interrumpe los demás
                    pass
        finally:
            # Marcar como enviada al terminar el lote (una única vez)
            Voluntariado.objects.filter(pk=voluntariado.pk).update(
                notificacion_activo_enviada_at=timezone.now()
            )

    # Ejecutar luego de commit, en otro hilo
    transaction.on_commit(lambda: threading.Thread(target=_send_all, daemon=True).start())
    return len(recipients)


def check_and_notify_activation(voluntariado: Voluntariado) -> int:
    """Si el voluntariado está activo y aún no se notificó, envía las notificaciones."""
    if not voluntariado.is_activo():
        return 0
    if voluntariado.notificacion_activo_enviada_at:
        return 0
    return notify_voluntariado_activated(voluntariado)
