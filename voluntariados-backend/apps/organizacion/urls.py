from rest_framework import routers
from django.urls import path, include
from .views import OrganizacionViewSet

router = routers.DefaultRouter()
router.register(r'organizaciones', OrganizacionViewSet, basename='organizacion')

urlpatterns = [path('', include(router.urls))]
