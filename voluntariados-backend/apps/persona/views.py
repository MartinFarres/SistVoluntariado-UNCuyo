from rest_framework import generics
from .models import Persona, Voluntario, Administrativo, Delegado
from .serializers import PersonaSerializer, VoluntarioSerializer, AdministrativoSerializer, DelegadoSerializer

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


class AdministrativoListCreateView(generics.ListCreateAPIView):
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer

class AdministrativoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer


class DelegadoListCreateView(generics.ListCreateAPIView):
    queryset = Delegado.objects.all()
    serializer_class = DelegadoSerializer

class DelegadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Delegado.objects.all()
    serializer_class = DelegadoSerializer