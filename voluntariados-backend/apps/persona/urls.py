from django.urls import path
from .views import PersonaListCreateView, PersonaDetailView
from .views import VoluntarioDetailView, VoluntarioListCreateView
from .views import AdministrativoDetailView, AdministrativoListCreateView
from .views import DelegadoDetailView, DelegadoListCreateView

urlpatterns = [
    path("", PersonaListCreateView.as_view(), name="persona-list-create"),
    path("<int:pk>/", PersonaDetailView.as_view(), name="persona-detail"),
    path("voluntario/", VoluntarioListCreateView.as_view(), name="voluntario-list-create"),
    path("voluntario/<int:pk>/", VoluntarioDetailView.as_view(), name="voluntario-detail"),
    path("administrativo/", AdministrativoListCreateView.as_view(), name="administrativo-list-create"),
    path("administrativo/<int:pk>/", AdministrativoDetailView.as_view(), name="administrativo-detail"),
    path("delegado/", DelegadoListCreateView.as_view(), name="delegado-list-create"),
    path("delegado/<int:pk>/", DelegadoDetailView.as_view(), name="delegado-detail"),
]

