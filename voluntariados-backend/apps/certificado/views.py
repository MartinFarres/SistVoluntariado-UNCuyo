import os
from datetime import datetime

from django.conf import settings
import logging
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader

from apps.asistencia.models import Asistencia
from apps.persona.models import Voluntario
from apps.voluntariado.models import InscripcionTurno, Voluntariado

logger = logging.getLogger(__name__)


# Permisos: solo Admin y Deleg pueden editar
class IsAdminOrDelegadoCreateEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("ADMIN", "DELEG")
        )


# Helper para cortar líneas de texto largo
def split_text(text, max_chars):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line + " " + word) > max_chars:
            lines.append(line.strip())
            line = word
        else:
            line += " " + word
    if line:
        lines.append(line.strip())
    return lines


# Subir / reemplazar plantilla
@api_view(["POST"])
@permission_classes([IsAdminOrDelegadoCreateEdit])
def upload_template(request):
    file = request.FILES.get("imagen")
    if not file:
        return Response({"detail": "No se envió ninguna imagen."}, status=400)

    # Validar extensión
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg"]:
        return Response({"detail": "Solo se permiten archivos PNG o JPG."}, status=400)

    # Validar tamaño
    if file.size > 2 * 1024 * 1024:  # 2 MB
        return Response({"detail": "El archivo no debe superar los 2 MB."}, status=400)

    # Guardar en media/plantillas/template_certificado.png (sobrescribe)
    plantillas_dir = os.path.join(settings.MEDIA_ROOT, "plantillas")
    os.makedirs(plantillas_dir, exist_ok=True)
    file_path = os.path.join(plantillas_dir, "template_certificado.png")

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return Response({"detail": "Plantilla actualizada correctamente."})


def generar_certificado_pdf(voluntario, voluntariado):
    # Delegate to generic generator by extracting values
    # Inscripciones
    inscripciones = InscripcionTurno.objects.filter(
        voluntario=voluntario,
        turno__voluntariado_id=voluntariado.id
    )
    if not inscripciones.exists():
        return None, "No se encontraron inscripciones para este voluntariado."

    # Total de horas
    total_horas = (
        Asistencia.objects
        .filter(inscripcion__in=inscripciones, presente=True)
        .aggregate(total=Sum('horas'))['total'] or 0
    )

    # Si no hay horas registradas, no generar certificado
    if not total_horas or float(total_horas) <= 0:
        return None, "No hay horas registradas para este voluntariado."

    # Último turno
    ultima_inscripcion = (
        inscripciones
        .select_related('turno')
        .order_by('-turno__fecha')
        .first()
    )
    ultima_fecha = ultima_inscripcion.turno.fecha
    ultimo_lugar = ultima_inscripcion.turno.lugar or '---'

    # Valores necesarios
    nombre = voluntario.nombre
    apellido = voluntario.apellido
    dni = voluntario.dni
    voluntariado_nombre = voluntariado.nombre
    fecha_fin = getattr(voluntariado, 'fecha_fin_cursado', None)

    return generar_certificado_pdf_from_values(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        voluntariado_nombre=voluntariado_nombre,
        fecha_fin_cursado=fecha_fin,
        ultima_fecha=ultima_fecha,
        ultimo_lugar=ultimo_lugar,
        total_horas=total_horas,
    )


def generar_certificado_pdf_from_values(
    *,
    nombre: str,
    apellido: str,
    dni: str,
    voluntariado_nombre: str,
    fecha_fin_cursado,
    ultima_fecha,
    ultimo_lugar: str,
    total_horas: float,
):
    """
    Generic PDF generator that accepts primitive values instead of model instances.
    Returns (HttpResponse, None) on success or (None, error_message) on failure.
    """
    # Plantilla
    fondo_path = os.path.join(settings.MEDIA_ROOT, "plantillas", "template_certificado.png")

    # PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"certificado_{apellido}_{nombre}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    width, height = landscape(A4)
    c = canvas.Canvas(response, pagesize=(width, height))

    # Fondo si existe
    if os.path.exists(fondo_path):
        c.drawImage(ImageReader(fondo_path), 0, 0, width=width, height=height)

    # Posiciones base
    offset_x = 210
    centro_x = width / 2
    centro_contenido = centro_x + offset_x / 2

    # Título
    c.setFont("Helvetica", 22)
    c.drawCentredString(centro_contenido, 420, "SE CERTIFICA QUE")

    # Nombre voluntario
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(centro_contenido, 380, f"{apellido}, {nombre}")

    # Texto 1
    texto1 = (
        f"con DNI {dni} ha participado en carácter de voluntario en el programa del "
        f"Voluntariado Universitario de la Universidad Nacional de Cuyo durante el ciclo {ultima_fecha.year}."
    )
    textobj = c.beginText()
    textobj.setTextOrigin(offset_x + centro_x - 400, 340)
    textobj.setFont("Helvetica", 14)
    textobj.setLeading(18)
    for line in split_text(texto1, 95):
        textobj.textLine(line)
    c.drawText(textobj)

    # Determinar si el voluntariado está activo o finalizado
    hoy = datetime.now().date()
    voluntariado_activo = bool(fecha_fin_cursado and fecha_fin_cursado > hoy)

    # Texto 2 (condicional)
    if voluntariado_activo:
        texto2 = (
            f"Las acciones actualmente son desempeñadas en “{voluntariado_nombre}”, en {ultimo_lugar}.\n"
            f"Al momento de emisión del certificado ha realizado una carga horaria de {total_horas} horas reloj."
        )
    else:
        texto2 = (
            f"Las acciones fueron desempeñadas en “{voluntariado_nombre}”, realizado en {ultimo_lugar}. "
            f"Totalizaron una carga horaria de {total_horas} horas reloj."
        )

    textobj = c.beginText()
    textobj.setTextOrigin(offset_x + centro_x - 400, 290)
    textobj.setFont("Helvetica", 14)
    textobj.setLeading(18)
    for line in split_text(texto2, 90):
        textobj.textLine(line)
    c.drawText(textobj)

    # Texto 3
    texto3 = (
        "Su participación activa dejó una huella positiva, destacando su contribución significativa a los objetivos de este programa."
    )
    textobj = c.beginText()
    textobj.setTextOrigin(offset_x + centro_x - 400, 250)
    textobj.setFont("Helvetica", 14)
    textobj.setLeading(18)
    for line in split_text(texto3, 95):
        textobj.textLine(line)
    c.drawText(textobj)

    # Fecha y ubicación (fecha en español)
    c.setFont("Helvetica", 12)
    now = datetime.now()
    meses_es = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    fecha_str = f"{now.strftime('%d')} de {meses_es[now.month - 1]} de {now.year}"
    c.drawRightString(width - 60, 200, fecha_str)
    c.drawRightString(width - 60, 185, "Universidad Nacional de Cuyo, Mendoza, Argentina")

    c.showPage()
    c.save()
    return response, None


def generar_certificado_para_usuario(voluntario_usuario, usuario, voluntariado_id):
    """
    Helper que valida el usuario actual y genera el PDF para el voluntariado.
    - voluntario_usuario: (optional) Voluntario instance resolved from usuario.persona
    - usuario: User instance (request.user)
    - voluntariado_id: id del voluntariado

    Retorna (HttpResponse, None) en éxito o (None, error_message) en fallo.
    """
    # Resolver voluntario asociado al usuario si no fue provisto
    if voluntario_usuario is None:
        voluntario_usuario = Voluntario.objects.filter(pk=getattr(usuario, "persona_id", None)).first()

    # Solo voluntarios pueden solicitar su propio certificado por este endpoint
    if not voluntario_usuario:
        return None, "No se encontró voluntario asociado a tu usuario."

    voluntariado = get_object_or_404(Voluntariado, pk=voluntariado_id)
    return generar_certificado_pdf(voluntario_usuario, voluntariado)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def generar_por_voluntariado(request, voluntariado_id=None):
    """
    Endpoint simple para que un voluntario autenticado genere su certificado
    para un voluntariado específico. Devuelve directamente el PDF.
    URL: GET /generacion/generar-por-voluntariado/<voluntariado_id>/
    """
    usuario = request.user
    try:
        response, error = generar_certificado_para_usuario(None, usuario, voluntariado_id)
    except Exception as e:
        # Unexpected exception (get_object_or_404 will normally raise Http404 and be handled by DRF)
        logger.exception(
            "Unexpected error while generating certificado for user=%s voluntariado=%s: %s",
            getattr(usuario, "id", None),
            voluntariado_id,
            e,
        )
        return Response({"detail": "Error interno al generar el certificado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if error:
        # Log the reason for easier debugging
        logger.warning(
            "Certificado generation denied for user=%s voluntariado=%s: %s",
            getattr(usuario, "id", None),
            voluntariado_id,
            error,
        )

        # Map common error messages to more appropriate HTTP status codes
        err_lower = (error or "").lower()
        if "inscripciones" in err_lower or "no se encontraron" in err_lower:
            status_code = status.HTTP_404_NOT_FOUND
        elif "no se encontró voluntario asociado" in err_lower or "no se encontró voluntario" in err_lower:
            # The user isn't a Voluntario (no persona) — not authorized to generate personal certificados
            status_code = status.HTTP_403_FORBIDDEN
        else:
            status_code = status.HTTP_403_FORBIDDEN

        return Response({"detail": error}, status=status_code)

    return response


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def horas_por_voluntariado(request, voluntariado_id=None):
    """
    Devuelve el total de horas registradas (presente=True) del voluntario asociado
    al usuario actual para el voluntariado indicado.
    URL: GET /generacion/horas-por-voluntariado/<voluntariado_id>/
    Response: { "total_horas": <number> }
    """
    usuario = request.user
    voluntario = Voluntario.objects.filter(pk=getattr(usuario, "persona_id", None)).first()
    if not voluntario:
        return Response({"detail": "No se encontró voluntario asociado a tu usuario."}, status=403)

    # Inscripciones para ese voluntariado
    inscripciones = InscripcionTurno.objects.filter(
        voluntario=voluntario,
        turno__voluntariado_id=voluntariado_id,
    )

    if not inscripciones.exists():
        return Response({"total_horas": 0}, status=200)

    total_horas = (
        Asistencia.objects
        .filter(inscripcion__in=inscripciones, presente=True)
        .aggregate(total=Sum('horas'))['total'] or 0
    )

    return Response({"total_horas": float(total_horas)}, status=200)


# Endpoint para generar desde Admin (DNI + voluntariado)
@api_view(["POST"])
@permission_classes([IsAdminOrDelegadoCreateEdit])
def generar_desde_admin(request):
    dni = request.data.get("dni")
    voluntariado_id = request.data.get("voluntariado_id")

    voluntario = Voluntario.objects.filter(dni=dni).first()
    if not voluntario:
        return Response({"detail": f"No se encontró voluntario con DNI {dni}."}, status=404)

    from apps.voluntariado.models import Voluntariado
    voluntariado = Voluntariado.objects.filter(id=voluntariado_id).first()
    if not voluntariado:
        return Response({"detail": "No se encontró el voluntariado."}, status=404)

    response, error = generar_certificado_pdf(voluntario, voluntariado)
    if error:
        return Response({"detail": error}, status=404)

    return response


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def generar_por_valores_admin(request):
    """
    Admin-only endpoint to generate a certificado from primitive values.
    Accepts JSON body with at least: nombre, apellido, dni, voluntariado_nombre,
    ultima_fecha (YYYY-MM-DD), ultimo_lugar, total_horas.
    Optional: fecha_fin_cursado (YYYY-MM-DD).
    Query param or JSON field 'format' can be 'pdf' (default) or 'image'. If 'image'
    is requested the view will try to convert the generated PDF to PNG and return it.
    If conversion dependencies are missing, it will fall back to returning PDF.
    """
    user = request.user
    if not (user and getattr(user, 'role', None) == 'ADMIN'):
        return Response({'detail': 'Solo administradores pueden usar este endpoint.'}, status=403)

    data = request.data
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    dni = data.get('dni')
    voluntariado_nombre = data.get('voluntariado_nombre')
    ultima_fecha_raw = data.get('ultima_fecha')
    ultimo_lugar = data.get('ultimo_lugar')
    total_horas_raw = data.get('total_horas')
    fecha_fin_raw = data.get('fecha_fin_cursado')

    # Basic validation
    missing = [k for k in ('nombre','apellido','dni','voluntariado_nombre','ultima_fecha','ultimo_lugar','total_horas') if not data.get(k)]
    if missing:
        return Response({'detail': f'Faltan campos requeridos: {",".join(missing)}'}, status=400)

    # Parse dates and numbers (expecting ISO YYYY-MM-DD for dates)
    try:
        ultima_fecha = datetime.strptime(ultima_fecha_raw, '%Y-%m-%d').date()
    except Exception:
        return Response({'detail': 'Formato de ultima_fecha inválido. Use YYYY-MM-DD.'}, status=400)

    fecha_fin_cursado = None
    if fecha_fin_raw:
        try:
            fecha_fin_cursado = datetime.strptime(fecha_fin_raw, '%Y-%m-%d').date()
        except Exception:
            return Response({'detail': 'Formato de fecha_fin_cursado inválido. Use YYYY-MM-DD.'}, status=400)

    try:
        total_horas = float(total_horas_raw)
    except Exception:
        return Response({'detail': 'total_horas debe ser numérico.'}, status=400)

    # Generate PDF (delegates to the generic function)
    response_pdf, error = generar_certificado_pdf_from_values(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        voluntariado_nombre=voluntariado_nombre,
        fecha_fin_cursado=fecha_fin_cursado,
    ultima_fecha=ultima_fecha,
        ultimo_lugar=ultimo_lugar,
        total_horas=total_horas,
    )
    if error:
        return Response({'detail': error}, status=400)

    return response_pdf
