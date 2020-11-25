from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('unemployed/<uuid:pk>/', views.UnemployedUserReadUpdateDeleteAPIView.as_view(), name='unemployed-detail'),
    path('unemployed/', views.UnemployedUserCreateAPIVIew.as_view(), name='unemployed-create'),
    path('<uuid:pk>/measurements/', views.MeasurementListCreateAPIView.as_view(), name='measurement-list'),
    path('<uuid:user_pk>/measurements/<uuid:measurement_pk>/',
         views.MeasurementReadUpdateDeleteAPIView.as_view(), name='measurement-detail')
]
