from django.shortcuts import render
from .models import Persona

def persona_list(request):
    personas = Persona.objects.all()
    return render(request, 'dashboard/personasTable.html', {'personas': personas})
