from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('<uuid:pk>/', views.UserReadUpdateDeleteAPIView.as_view(), name='detail'),
    path('', views.UserCreateAPIVIew.as_view(), name='create'),
    path('update-password/', views.update_user_password, name='update-password')
]
