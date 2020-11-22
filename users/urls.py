from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('unemployed/<uuid:pk>/', views.UnemployedUserReadUpdateDeleteAPIView.as_view(), name='unemployed-detail'),
    path('unemployed/', views.UnemployedUserCreateAPIVIew.as_view(), name='unemployed-create'),
    path('<uuid:pk>/price/', views.GetUserInsurancePrice.as_view(), name='price')
]
