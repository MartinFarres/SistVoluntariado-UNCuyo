from django.urls import path
from .views import PowerBIDashboardView, APIKeyView

urlpatterns = [
    path('powerbi/', PowerBIDashboardView.as_view(), name='powerbi_dashboard'),
    path('powerbi/key/', APIKeyView.as_view(), name='powerbi_api_key'),
]
