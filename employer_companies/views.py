from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView

from users.models import EmployedUser, EmployerCompanyRepresentative
from users.serializers import EmployedUserCreateSerializer, EmployedUserSerializer
from .models import EmployerCompany
from users.serializers import EmployerCompanyRepresentativeCreateSerializer, EmployerCompanyRepresentativeSerializer


class EmployedUserListCreateAPIVIew(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployedUserCreateSerializer
        return EmployedUserSerializer

    def get_queryset(self):
        employer_company_pk = self.kwargs['pk']
        employer_company = get_object_or_404(EmployerCompany, pk=employer_company_pk)
        return EmployedUser.objects.filter(employer_company=employer_company)

    def perform_create(self, serializer):
        employer_company_pk = self.kwargs['pk']
        employer_company = get_object_or_404(EmployerCompany, pk=employer_company_pk)
        insurance_company = employer_company.insurance_company
        serializer.save(employer_company=employer_company, insurance_company=insurance_company)


class EmployedUserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmployedUser.objects.all()
    serializer_class = EmployedUserSerializer
    lookup_url_kwarg = 'employee_pk'


class EmployerCompanyRepresentativeListCreateAPIView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployerCompanyRepresentativeCreateSerializer
        return EmployerCompanyRepresentativeSerializer

    def get_queryset(self):
        employer_company_pk = self.kwargs['pk']
        employer_company = get_object_or_404(EmployerCompany, pk=employer_company_pk)
        return EmployerCompanyRepresentative.objects.filter(employer_company=employer_company)

    def perform_create(self, serializer):
        employer_company_pk = self.kwargs['pk']
        employer_company = get_object_or_404(EmployerCompany, pk=employer_company_pk)
        insurance_company = employer_company.insurance_company
        serializer.save(employer_company=employer_company, insurance_company=insurance_company)


class EmployerCompanyRepresentativeReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmployerCompanyRepresentative.objects.all()
    serializer_class = EmployerCompanyRepresentativeSerializer
    lookup_url_kwarg = 'representative_pk'


