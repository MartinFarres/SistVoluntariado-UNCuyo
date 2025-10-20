from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.permissions import IsAdminUser

from apps.persona.models import Voluntario
from apps.voluntariado.models import Voluntariado
from apps.certificado.models import Certificado
from apps.facultad.models import Facultad


class PowerBIDashboardView(APIView):
    """
    Endpoint consolidado con datos relevantes para Power BI.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # Estadísticas Generales
        total_voluntarios = Voluntario.objects.count()
        voluntariados_activos = Voluntariado.objects.filter(estado='ACTIVE').count()
        certificados_emitidos = Certificado.objects.count()

        # Voluntarios por Facultad
        voluntarios_por_facultad = list(
            Facultad.objects.annotate(
                voluntarios_count=Count('carreras__voluntario', distinct=True)
            ).values('nombre', 'voluntarios_count').order_by('-voluntarios_count')
        )

        # Estado de Voluntariados
        estado_voluntariados_query = Voluntariado.objects.values('estado').annotate(count=Count('id'))
        estado_voluntariados = {
            'draft': 0,
            'active': 0,
            'closed': 0,
        }
        for item in estado_voluntariados_query:
            estado = item['estado'].lower()
            if estado in estado_voluntariados:
                estado_voluntariados[estado] = item['count']

        # Ensamblar el JSON de respuesta
        data = {
            'stats_generales': {
                'total_voluntarios': total_voluntarios,
                'voluntariados_activos': voluntariados_activos,
                'certificados_emitidos': certificados_emitidos,
            },
            'voluntarios_por_facultad': voluntarios_por_facultad,
            'estado_voluntariados': estado_voluntariados,
        }

        return Response(data, status=status.HTTP_200_OK)
