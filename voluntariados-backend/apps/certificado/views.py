import os
from datetime import datetime

from django.conf import settings
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


# 🔐 Permisos: solo Admin y Deleg pueden editar
class IsAdminOrDelegadoCreateEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("ADMIN", "DELEG")
        )


# 📝 Helper para cortar líneas de texto largo
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


# 📤 Subir / reemplazar plantilla
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
    # 📌 Inscripciones
    inscripciones = InscripcionTurno.objects.filter(
        voluntario=voluntario,
        turno__voluntariado_id=voluntariado.id
    )
    if not inscripciones.exists():
        return None, "No se encontraron inscripciones para este voluntariado."

    # ⏳ Total de horas
    total_horas = (
        Asistencia.objects
        .filter(inscripcion__in=inscripciones, presente=True)
        .aggregate(total=Sum('horas'))['total'] or 0
    )

    # 📅 Último turno
    ultima_inscripcion = (
        inscripciones
        .select_related('turno')
        .order_by('-turno__fecha')
        .first()
    )
    ultima_fecha = ultima_inscripcion.turno.fecha
    ultimo_lugar = ultima_inscripcion.turno.lugar or '---'

    # 🖼️ Plantilla
    fondo_path = os.path.join(settings.MEDIA_ROOT, "plantillas", "template_certificado.png")

    # 📄 PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"certificado_{voluntario.apellido}_{voluntario.nombre}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    width, height = landscape(A4)
    c = canvas.Canvas(response, pagesize=(width, height))

    # 🖼️ Fondo si existe
    if os.path.exists(fondo_path):
        c.drawImage(ImageReader(fondo_path), 0, 0, width=width, height=height)

    # 📐 Posiciones base
    offset_x = 210
    centro_x = width / 2
    centro_contenido = centro_x + offset_x / 2

    # 📌 Título
    c.setFont("Helvetica", 22)
    c.drawCentredString(centro_contenido, 420, "SE CERTIFICA QUE")

    # 📌 Nombre voluntario
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(
        centro_contenido, 380,
        f"{voluntario.apellido}, {voluntario.nombre}"
    )

    # 📝 Texto 1
    texto1 = (
        f"con DNI {voluntario.dni} ha participado en carácter de voluntario en el programa del "
        f"Voluntariado Universitario de la Universidad Nacional de Cuyo durante el ciclo {ultima_fecha.year}."
    )
    textobj = c.beginText()
    textobj.setTextOrigin(offset_x + centro_x - 400, 340)
    textobj.setFont("Helvetica", 14)
    textobj.setLeading(18)
    for line in split_text(texto1, 95):
        textobj.textLine(line)
    c.drawText(textobj)

    # 🧩 Determinar si el voluntariado está activo o finalizado
    fecha_fin = voluntariado.fecha_fin_cursado
    hoy = datetime.now().date()
    voluntariado_activo = fecha_fin and fecha_fin > hoy

    # 📝 Texto 2 (condicional)
    if voluntariado_activo:
        texto2 = (
            f"Las acciones actualmente son desempeñadas en “{voluntariado.nombre}”, en {ultimo_lugar}.\n"
            f"Al momento de emisión del certificado ha realizado una carga horaria de {total_horas} horas reloj."
        )
    else:
        texto2 = (
            f"Las acciones fueron desempeñadas en “{voluntariado.nombre}”, realizado en {ultimo_lugar}. "
            f"Totalizaron una carga horaria de {total_horas} horas reloj."
        )

    textobj = c.beginText()
    textobj.setTextOrigin(offset_x + centro_x - 400, 290)
    textobj.setFont("Helvetica", 14)
    textobj.setLeading(18)
    for line in split_text(texto2, 90):
        textobj.textLine(line)
    c.drawText(textobj)

    # 📝 Texto 3
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

    # 📅 Fecha y ubicación
    c.setFont("Helvetica", 12)
    c.drawRightString(width - 60, 200, datetime.now().strftime("%d de %B de %Y"))
    c.drawRightString(width - 60, 185, "Universidad Nacional de Cuyo, Mendoza, Argentina")

    c.showPage()
    c.save()
    return response, None


# 🧾 Endpoint para voluntarios autenticados
class CertificadoGeneracionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        methods=["get"],
        url_path="generar-por-voluntariado/(?P<voluntariado_id>[^/.]+)"
    )
    def generar_por_voluntariado(self, request, voluntariado_id=None):
        usuario = request.user

        voluntario_objetivo = Voluntario.objects.filter(
            pk=getattr(usuario, "persona_id", None)
        ).first()
        if not (voluntario_objetivo or usuario.role in ("ADMIN", "DELEG")):
            return Response(
                {"detail": "No se encontró voluntario asociado a tu usuario."},
                status=status.HTTP_403_FORBIDDEN
            )

        voluntariado = get_object_or_404(Voluntariado, pk=voluntariado_id)
        response, error = generar_certificado_pdf(voluntario_objetivo, voluntariado)
        if error:
            return Response({"detail": error}, status=404)
        return response


# 🧾 Endpoint para generar desde Admin (DNI + voluntariado)
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
