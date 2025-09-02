from django.urls import path

from .views import persona_list, persona_create

urlpatterns = [
    path("", persona_list, name="persona_list"),
    path("persona/create", persona_create, name="persona_create"),
]