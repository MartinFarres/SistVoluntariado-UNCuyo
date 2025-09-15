from rest_framework import generics
from .models import Persona, Voluntario
from .serializers import PersonaSerializer, VoluntarioSerializer

# Listar y crear personas
class PersonaListCreateView(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

# Ver, actualizar y eliminar persona individual
class PersonaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer



class VoluntarioListCreateView(generics.ListCreateAPIView):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer

class VoluntarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer