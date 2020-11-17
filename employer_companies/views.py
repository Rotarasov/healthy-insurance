from rest_framework.generics import ListAPIView, CreateAPIView

from users.models import User, EmployedUser
from users.serializers import UserCreateSerializer
from .serializers import EmployerCompanySerializer


class EmployeesListAPIVIew(ListAPIView):
    serializer_class = EmployerCompanySerializer

    def get_queryset(self):
        employer_company = self.get_object()
        return EmployedUser.objects.filter(employer_company_id=employer_company.id)


class EmployeeCreateAPIVIew(CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data['role'] = User.Roles.EMPLOYED
        return super().create(request, *args, **kwargs)



