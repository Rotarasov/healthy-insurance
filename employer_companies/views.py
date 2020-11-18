from rest_framework.generics import ListAPIView, get_object_or_404

from users.serializers import UserSerializer
from .models import EmployerCompany


class EmployeesListAPIVIew(ListAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])

    def get_queryset(self):
        employer_company = self.get_object()
        return employer_company.employees
