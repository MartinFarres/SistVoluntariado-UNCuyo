from django.urls import path
from .views import PersonaListCreateView, PersonaDetailView
from .views import VoluntarioDetailView, VoluntarioListCreateView

urlpatterns = [
    path("", PersonaListCreateView.as_view(), name="persona-list-create"),
    path("<int:pk>/", PersonaDetailView.as_view(), name="persona-detail"),
    path("voluntario/", VoluntarioListCreateView.as_view(), name="voluntario-list-create"),
    path("voluntario/<int:pk>/", VoluntarioDetailView.as_view(), name="voluntario-detail"),

]

