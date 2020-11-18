from django.urls import path

from . import views

app_name = 'employer_companies'

urlpatterns = [
    path('<uuid:pk>/employees/', views.EmployeesListAPIVIew.as_view(), name='employees'),
]