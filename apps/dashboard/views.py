from django.shortcuts import render
from .models import Persona
from .forms import PersonaForm
from django.shortcuts import redirect
from django.urls import reverse

def persona_list(request):
    personas = Persona.objects.all()
    return render(request, 'dashboard/personasTable.html', {'personas': personas})


def persona_create(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        
        if form.is_valid():
            dni = form.cleaned_data['dni']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            persona = Persona()
            persona.dni = dni
            persona.name = name
            persona.surname = surname
            persona.save()

            return redirect(reverse('persona_list'))
    else:
        form = PersonaForm()
    return render(request, 'dashboard/persona/form.html', {'form': form})