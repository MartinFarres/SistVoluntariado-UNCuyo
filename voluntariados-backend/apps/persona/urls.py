from django.urls import path
from .views import PersonaListCreateView, PersonaDetailView
from .views import VoluntarioDetailView, VoluntarioListCreateView
from .views import AdministrativoDetailView, AdministrativoListCreateView
from .views import DelegadoDetailView, DelegadoListCreateView
from .views import GestionadorDetailView, GestionadorListCreateView

urlpatterns = [
    path("", PersonaListCreateView.as_view(), name="persona-list-create"),
    path("<int:pk>/", PersonaDetailView.as_view(), name="persona-detail"),
    path("gestionador/", GestionadorListCreateView.as_view(), name="gestionador-list-create"),
    path("gestionador/<int:pk>/", GestionadorDetailView.as_view(), name="gestionador-detail"),
    path("voluntario/", VoluntarioListCreateView.as_view(), name="voluntario-list-create"),
    path("voluntario/<int:pk>/", VoluntarioDetailView.as_view(), name="voluntario-detail"),
    path("administrativo/", AdministrativoListCreateView.as_view(), name="administrativo-list-create"),
    path("administrativo/<int:pk>/", AdministrativoDetailView.as_view(), name="administrativo-detail"),
    path("delegado/", DelegadoListCreateView.as_view(), name="delegado-list-create"),
    path("delegado/<int:pk>/", DelegadoDetailView.as_view(), name="delegado-detail"),
]

