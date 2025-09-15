from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404

from .models import Certificado
from .serializers import CertificadoSerializer


class IsAdminOrDelegadoCreateEdit(permissions.BasePermission):
    """
    Permite crear/editar certificados solo a users con role ADMIN o DELEG.
    Lectura/downlaod: usuario autenticado.
    Ajustá según tu política de roles.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # GET/HEAD/OPTIONS -> cualquier usuario autenticado puede leer
            return request.user and request.user.is_authenticated
        # Métodos no seguros -> crear/editar/eliminar: sólo ADMIN o DELEG
        return request.user and request.user.is_authenticated and request.user.role in ("ADMIN", "DELEG")

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class CertificadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Certificado.
    Endpoints principales:
      - GET /api/certificados/                -> list
      - POST /api/certificados/               -> create (ADMIN/DELEG)
      - GET /api/certificados/{pk}/           -> retrieve
      - PUT/PATCH /api/certificados/{pk}/     -> update (ADMIN/DELEG)
      - DELETE /api/certificados/{pk}/        -> destroy (ADMIN/DELEG)
      - GET /api/certificados/{pk}/download/  -> descarga el archivo (autenticado)
    """
    queryset = Certificado.objects.select_related("voluntario__persona", "voluntariado", "creado_por").all()
    serializer_class = CertificadoSerializer
    permission_classes = [IsAdminOrDelegadoCreateEdit]

    def perform_create(self, serializer):
        # Asignamos el creador del certificado automáticamente
        serializer.save(creado_por=self.request.user)

    def perform_update(self, serializer):
        # Actualizamos quien lo editó (si querés conservar historial, usá otro campo o log)
        serializer.save(creado_por=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        """
        Devuelve el archivo adjunto del certificado como FileResponse (attachment).
        Si no hay archivo asociado devuelve 404 con mensaje. 
        """
        certificado = get_object_or_404(Certificado, pk=pk)

        # Opcional: chequeo de permisos por objeto (ej: sólo volunteers dueños o admins pueden descargar)
        # if request.user.role not in ("ADMIN", "DELEG") and certificado.persona.persona.user != request.user:
        #     return Response({"detail": "No tienes permiso para descargar este certificado."}, status=status.HTTP_403_FORBIDDEN)

        if not certificado.archivo:
            return Response(
                {"detail": "No existe un archivo para este certificado. Generá el PDF antes de intentar descargar."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # FileField devuelve un FieldFile; usamos open() para FileResponse
            return FileResponse(certificado.archivo.open("rb"), as_attachment=True, filename=certificado.archivo.name.split("/")[-1])
        except Exception as e:
            # devolver error genérico si no pudo abrirse
            return Response({"detail": f"Error al leer el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Si querés agregar una acción para generar el PDF on-demand, podés crear un @action POST 'generate'
# que:
#  - calcule las horas (si corresponde)
#  - genere un PDF (ReportLab / WeasyPrint / xhtml2pdf)
#  - guarde el PDF en Certificado.archivo
#  - devuelva la representación del certificado
#
# EJEMPLO (pseudocódigo):
# @action(detail=True, methods=['post'], permission_classes=[IsAdminOrDelegadoCreateEdit])
# def generate(self, request, pk=None):
#     cert = self.get_object()
#     # 1) calcular horas si es necesario
#     # 2) renderizar HTML + convertir a PDF (weasyprint.HTML(string=html).write_pdf())
#     # 3) guardar en cert.archivo.save('cert_..pdf', ContentFile(pdf_bytes))
#     # 4) return Response(CertificadoSerializer(cert).data)
#
# Requiere instalar y configurar una librería de generación de PDF.
