from rest_framework import routers
from django.urls import path, include
from .views import VoluntarioViewSet

router = routers.DefaultRouter()
router.register(r'voluntarios', VoluntarioViewSet, basename='voluntarios')

urlpatterns = [path('', include(router.urls))]
