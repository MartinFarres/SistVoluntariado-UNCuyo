from rest_framework import generics
from .models import Persona
from .serializers import PersonaSerializer

# Listar y crear personas
class PersonaListCreateView(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

# Ver, actualizar y eliminar persona individual
class PersonaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
