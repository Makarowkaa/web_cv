from django.urls import path

from .views import CompanyView, CompanyListView, CompanyDetailsView

urlpatterns = [
    path('', CompanyView.as_view(), name='companies'),
    path('all/', CompanyListView.as_view(), name='all-companies'),
    path('details/<int:pk>/', CompanyDetailsView.as_view(), name='company-details'),
]