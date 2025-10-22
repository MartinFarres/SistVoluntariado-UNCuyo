from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from apps.persona.models import Voluntario
from .serializers import VoluntarioPowerBISerializer, APIKeySerializer
from .models import APIKey
from .permissions import HasAPIKey


class PowerBIDashboardView(APIView):
    """
    Endpoint que devuelve una lista detallada de todos los voluntarios para Power BI.
    Requiere una clave de API válida para el acceso.
    """
    permission_classes = [HasAPIKey] # Usamos el nuevo permiso de clave de API

    def get(self, request, format=None):
        queryset = Voluntario.objects.select_related(
            'carrera__facultad',
            'localidad__departamento__provincia'
        ).all()
        serializer = VoluntariadoPowerBISerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIKeyView(APIView):
    """
    Vista para que los administradores gestionen su clave de API para Power BI.
    """
    permission_classes = [IsAdminUser]
    serializer_class = APIKeySerializer

    def get(self, request, format=None):
        """
        Obtiene la clave de API existente del usuario o crea una nueva si no existe.
        """
        api_key, created = APIKey.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(api_key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Genera una nueva clave de API, invalidando la anterior.
        """
        APIKey.objects.filter(user=request.user).delete()
        new_api_key = APIKey.objects.create(user=request.user)
        serializer = self.serializer_class(new_api_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
