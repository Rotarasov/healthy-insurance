from django.urls import path

from . import views

app_name = 'employer_companies'

urlpatterns = [
    path('', views.EmployerCompanyListCreateAPIView.as_view(), name='company-list'),
    path('<uuid:pk>', views.EmployerCompanyReadUpdateDeleteAPIView.as_view(), name='company-detail'),
    path('<uuid:pk>/employees/', views.EmployedUserListCreateAPIVIew.as_view(), name='employee-list'),
    path('<uuid:employer_company_pk>/employees/<uuid:employee_pk>',
         views.EmployedUserReadUpdateDeleteAPIView.as_view(), name='employee-detail'),
    path('<uuid:pk>/representatives/',
         views.EmployerCompanyRepresentativeListCreateAPIView.as_view(), name='representative-list'),
    path('<uuid:employer_company_pk>/representatives/<uuid:representative_pk>/',
         views.EmployerCompanyRepresentativeReadUpdateDeleteAPIView.as_view(), name='representative-detail'),
    path('<uuid:pk>/prices/', views.EmployerCompanyCoveragePriceListAPIView.as_view(), name='price-list')
]