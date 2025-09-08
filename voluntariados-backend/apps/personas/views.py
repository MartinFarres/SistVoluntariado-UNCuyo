from rest_framework import viewsets, permissions
from .models import Persona
from .serializers import PersonaSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all().select_related("localidad")
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # podés filtrar por dni, apellido, etc. más adelante
    def get_queryset(self):
        queryset = super().get_queryset()
        # Aquí podrías agregar lógica para filtrar por parámetros de consulta
        dni = self.request.query_params.get('dni', None)
        if dni is not None:
            queryset = queryset.filter(dni=dni)
        # Agrega más filtros según sea necesario    
        return queryset
    
