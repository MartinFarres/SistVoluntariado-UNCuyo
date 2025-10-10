from django.urls import path
from .views import PaisListCreateView, PaisDetailView
from .views import ProvinciaListCreateView, ProvinciaDetailView
from .views import DepartamentoListCreateView, DepartamentoDetailView
from .views import LocalidadListCreateView, LocalidadDetailView

urlpatterns = [
    path("pais/", PaisListCreateView.as_view(), name="pais-list-create"),
    path("pais/<int:pk>/", PaisDetailView.as_view(), name="pais-detail"),
    path("provincia/", ProvinciaListCreateView.as_view(), name="provincia-list-create"),
    path("provincia/<int:pk>/", ProvinciaDetailView.as_view(), name="provincia-detail"),
    path("departamento/", DepartamentoListCreateView.as_view(), name="departamento-list-create"),
    path("departamento/<int:pk>/", DepartamentoDetailView.as_view(), name="departamento-detail"),
    path("localidad/", LocalidadListCreateView.as_view(), name="localidad-list-create"),
    path("localidad/<int:pk>/", LocalidadDetailView.as_view(), name="localidad-detail")
]


