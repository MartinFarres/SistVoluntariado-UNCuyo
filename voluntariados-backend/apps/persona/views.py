from rest_framework import generics, permissions
from .models import Persona, Voluntario, Administrativo, Delegado
from .serializers import PersonaSerializer, VoluntarioSerializer, AdministrativoSerializer, DelegadoSerializer
from apps.users.permissions import IsAdministrador

# Listar y crear personas
class PersonaListCreateView(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAdministrador]

# Ver, actualizar y eliminar persona individual
class PersonaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAdministrador]

class VoluntarioListCreateView(generics.ListCreateAPIView):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer
    permission_classes = [IsAdministrador]


class VoluntarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer
    permission_classes = [IsAdministrador]


class AdministrativoListCreateView(generics.ListCreateAPIView):
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer
    permission_classes = [IsAdministrador]

class AdministrativoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrativo.objects.all()
    serializer_class = AdministrativoSerializer
    permission_classes = [IsAdministrador]

class DelegadoListCreateView(generics.ListCreateAPIView):
    queryset = Delegado.objects.all()
    serializer_class = DelegadoSerializer
    permission_classes = [IsAdministrador]

class DelegadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Delegado.objects.all()
    serializer_class = DelegadoSerializer
    permission_classes = [IsAdministrador]
