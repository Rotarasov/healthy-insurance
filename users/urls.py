from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'

urlpatterns = [
    path('unemployed/<uuid:pk>/', views.UnemployedUserReadUpdateDeleteAPIView.as_view(), name='unemployed-detail'),
    path('unemployed/', views.UnemployedUserCreateAPIVIew.as_view(), name='unemployed-create'),
    path('<uuid:pk>/measurements/', views.MeasurementListCreateAPIView.as_view(), name='measurement-list'),
    path('<uuid:user_pk>/measurements/<uuid:measurement_pk>/',
         views.MeasurementReadUpdateDeleteAPIView.as_view(), name='measurement-detail'),
    path('<uuid:pk>/price/', views.GetLatestUserInsurancePrice.as_view(), name='insurance-price'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh')
]
