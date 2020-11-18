from rest_framework.generics import ListCreateAPIView, get_object_or_404

from users.serializers import UserSerializer, EmployedUserCreateSerializer
from .models import EmployerCompany


class EmployeesListAPIVIew(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployedUserCreateSerializer
        return UserSerializer

    def get_object(self):
        return get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])

    def get_queryset(self):
        employer_company = self.get_object()
        return employer_company.employees
