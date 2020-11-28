from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('employer-companies/', include('employer_companies.urls')),
    path('insurance-companies/', include('insurance_companies.urls'))
]
