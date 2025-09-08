from rest_framework import routers
from django.urls import path, include
from .views import PersonaViewSet

router = routers.DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona')

urlpatterns = [path('', include(router.urls))]
