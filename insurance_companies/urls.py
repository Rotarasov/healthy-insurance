from django.urls import path

from . import views


app_name = 'insurance_companies'

urlpatterns = [
    path('', views.InsuranceCompanyCreateAPIView.as_view(), name='create'),
    path('<uuid:pk>/', views.InsuranceCompanyReadUpdateDeleteAPIVIew.as_view(), name='detail'),
    path('<uuid:pk>/clients/', views.InsuranceCompanyClientsListAPIView.as_view(), name='clients'),
    path('<uuid:pk>/companies/', views.InsuranceCompanyPartnerCompaniesAPIVIew.as_view(), name='companies')
]