from django.urls import path
from .views import (
    PaisViewSet,
    ProvinciaViewSet,
    DepartamentoViewSet,
    LocalidadViewSet,
)

urlpatterns = [
    # Keep the same URL structure but map to the ViewSet actions so existing clients don't break
    path("pais/", PaisViewSet.as_view({"get": "list", "post": "create"}), name="pais-list-create"),
    path("pais/<int:pk>/", PaisViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="pais-detail"),

    path("provincia/", ProvinciaViewSet.as_view({"get": "list", "post": "create"}), name="provincia-list-create"),
    path("provincia/<int:pk>/", ProvinciaViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="provincia-detail"),

    path("departamento/", DepartamentoViewSet.as_view({"get": "list", "post": "create"}), name="departamento-list-create"),
    path("departamento/<int:pk>/", DepartamentoViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="departamento-detail"),

    path("localidad/", LocalidadViewSet.as_view({"get": "list", "post": "create"}), name="localidad-list-create"),
    path("localidad/<int:pk>/", LocalidadViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="localidad-detail"),
]


