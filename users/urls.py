from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('unemployed/<uuid:pk>/', views.UnemployedUserReadUpdateDeleteAPIView.as_view(), name='unemployed-detail'),
    path('unemployed/', views.UnemployedUserCreateAPIVIew.as_view(), name='unemployed-create'),
    path('employer-company-representative/<uuid:pk>/',
         views.EmployerCompanyRepresentativeReadUpdateDeleteAPIView.as_view(),
         name='employer-company-representative-detail'),
    path('employer-company-representative/',
         views.EmployerCompanyRepresentativeCreateAPIView.as_view(),
         name='employer-company-representative-create'),
    path('employed/<uuid:pk>/', views.EmployedUserReadUpdateDeleteAPIView.as_view(), name='employed-detail')
]
