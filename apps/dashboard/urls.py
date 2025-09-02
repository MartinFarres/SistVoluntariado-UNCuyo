from django.urls import path

from .views import persona_list

urlpatterns = [
    path("", persona_list, name="persona_list"),
]