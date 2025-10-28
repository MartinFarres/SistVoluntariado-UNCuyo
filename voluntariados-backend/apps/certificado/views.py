import os

from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

from rest_framework import viewsets
from apps.asistencia.models import Asistencia
from apps.certificado.models import EncabezadoCertificado
from .models import Certificado, Autoridad
from .serializers import CertificadoSerializer, AutoridadSerializer, EncabezadoCertificadoSerializer
from ..persona.models import Voluntario
from ..voluntariado.models import InscripcionTurno


class IsAdminOrDelegadoCreateEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("ADMIN", "DELEG")
        )

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

def get_media_path(file_field):
    """Devuelve la ruta absoluta desde MEDIA_ROOT para un FileField/ImageField."""
    if file_field and hasattr(file_field, 'name'):
        return os.path.join(settings.MEDIA_ROOT, file_field.name)
    return None

class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = Certificado.objects.select_related("asistencia").prefetch_related("autoridades").all()
    serializer_class = CertificadoSerializer
    permission_classes = [IsAdminOrDelegadoCreateEdit]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        url_path="generar-por-voluntariado/(?P<voluntariado_id>[^/.]+)",
        permission_classes=[permissions.IsAuthenticated]
    )
    def generar_por_voluntariado(self, request, voluntariado_id=None):
        usuario = request.user

        # 🔐 Validación de usuario voluntario o admin
        voluntario_objetivo = Voluntario.objects.filter(pk=getattr(usuario, "persona_id", None)).first()
        if not (voluntario_objetivo or usuario.role in ("ADMIN", "DELEG")):
            return Response({"detail": "No se encontró voluntario asociado a tu usuario."},
                            status=status.HTTP_403_FORBIDDEN)

        # 📝 Obtener inscripción y asistencia
        inscripcion = get_object_or_404(
            InscripcionTurno,
            voluntario=voluntario_objetivo,
            turno__voluntariado_id=voluntariado_id
        )
        turno = inscripcion.turno
        asistencia = get_object_or_404(Asistencia, inscripcion=inscripcion)
        # 🆕 Crear certificado si no existe
        certificado, creado = Certificado.objects.get_or_create(
            asistencia=asistencia,
            defaults={"creado_por": request.user}
        )

        autoridades = Autoridad.objects.all()[:3]
        if creado:
            certificado.autoridades.set(autoridades)

        voluntariado = inscripcion.turno.voluntariado
        encabezado = EncabezadoCertificado.objects.order_by('-actualizado').first()

        # 📄 Generar PDF
        response = HttpResponse(content_type='application/pdf')
        filename = f"certificado_{voluntario_objetivo.apellido}_{voluntario_objetivo.nombre}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        width, height = landscape(A4)
        c = canvas.Canvas(response, pagesize=(width, height))

        # 🖼️ Fondo
        fondo_path = os.path.join(settings.MEDIA_ROOT, "plantillas", "template_certificado.png")
        if os.path.exists(fondo_path):
            c.drawImage(ImageReader(fondo_path), 0, 0, width=width, height=height)

        # 📐 Offset horizontal (ajustado más a la derecha)
        offset_x = 210
        centro_x = width / 2
        centro_contenido = centro_x + offset_x / 2

        # 🖼️ Encabezado (zona roja) — más compacto
        if encabezado:
            encabezado_y = 520
            encabezado_altura = 70
            encabezado_anchura = 180  # más angostas
            posiciones_x_enc = [
                centro_contenido - 200,
                centro_contenido - 70,
                centro_contenido + 70,
                centro_contenido + 200
            ]

            imagenes = [encabezado.imagen_1, encabezado.imagen_2, encabezado.imagen_3, encabezado.imagen_4]
            for i, img_field in enumerate(imagenes):
                img_path = get_media_path(img_field)
                if img_path and os.path.exists(img_path):
                    c.drawImage(
                        img_path,
                        posiciones_x_enc[i] - encabezado_anchura / 2,
                        encabezado_y,
                        width=120,
                        height=encabezado_altura,
                        mask='auto',
                        preserveAspectRatio=True
                    )

        # 📌 Título
        c.setFont("Helvetica", 22)
        c.drawCentredString(centro_contenido, 420, "SE CERTIFICA QUE")

        # 📌 Nombre voluntario
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(centro_contenido, 380, f"{voluntario_objetivo.apellido}, {voluntario_objetivo.nombre}")

        # 📝 Texto 1
        texto1 = (
            f"con DNI {voluntario_objetivo.dni} ha participado en carácter de voluntario en el programa del "
            f"Voluntariado Universitario de la Universidad Nacional de Cuyo durante el ciclo {turno.fecha.year}."
        )
        textobj = c.beginText()
        textobj.setTextOrigin(offset_x + centro_x - 400, 340)
        textobj.setFont("Helvetica", 14)
        textobj.setLeading(18)
        for line in split_text(texto1, 95):
            textobj.textLine(line)
        c.drawText(textobj)

        # 📝 Texto 2
        texto2 = (
            f"Las acciones fueron desempeñadas en “{voluntariado.nombre}”, realizado en {inscripcion.turno.lugar}. "
            f"Totalizaron una carga horaria de {asistencia.horas} horas reloj."
        )
        textobj = c.beginText()
        textobj.setTextOrigin(offset_x + centro_x - 400, 290)
        textobj.setFont("Helvetica", 14)
        textobj.setLeading(18)
        for line in split_text(texto2, 95):
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

        # 🖊️ Firmas (zona amarilla)
        firma_y = 120
        firma_ancho = 180
        firma_alto = 60
        posiciones_x = [
            centro_contenido - 200,
            centro_contenido,
            centro_contenido + 200
        ]

        for i, autoridad in enumerate(autoridades[:3]):
            firma_path = get_media_path(autoridad.firma)
            if firma_path and os.path.exists(firma_path):
                c.drawImage(
                    firma_path,
                    posiciones_x[i] - firma_ancho / 2,
                    firma_y,
                    width=firma_ancho,
                    height=firma_alto,
                    mask='auto',
                    preserveAspectRatio=True
                )

        # 👤 Nombre y cargo autoridades
        c.setFont("Helvetica-Bold", 12)
        nombre_y = 90
        detalle_y = 75
        for i, autoridad in enumerate(autoridades[:3]):
            c.drawCentredString(
                posiciones_x[i],
                nombre_y,
                f"{autoridad.nombre.upper()} {autoridad.apellido.upper()}"
            )
            c.setFont("Helvetica", 10)
            c.drawCentredString(
                posiciones_x[i],
                detalle_y,
                f"{autoridad.cargo.upper()} - {autoridad.entidad_encargada}"
            )

        c.showPage()
        c.save()
        return response


class AutoridadViewSet(viewsets.ModelViewSet):
    queryset = Autoridad.objects.all()
    serializer_class = AutoridadSerializer
    permission_classes = [IsAdminOrDelegadoCreateEdit]

class EncabezadoCertificadoViewSet(viewsets.ModelViewSet):
    queryset = EncabezadoCertificado.objects.all().order_by('-actualizado')
    serializer_class = EncabezadoCertificadoSerializer
    permission_classes = [IsAdminOrDelegadoCreateEdit]

