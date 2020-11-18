from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404

from employer_companies.models import EmployerCompany
from employer_companies.serializers import EmployerCompanySerializer
from users.serializers import UserSerializer
from .models import InsuranceCompany
from .serializers import InsuranceCompanySerializer


User = get_user_model()


class InsuranceCompanyCreateAPIView(CreateAPIView):
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer


class InsuranceCompanyReadUpdateDeleteAPIVIew(RetrieveUpdateDestroyAPIView):
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer


class InsuranceCompanyClientsListAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(InsuranceCompany, pk=self.kwargs['pk'])

    def get_queryset(self):
        insurance_company = self.get_object()
        return insurance_company.clients


class InsuranceCompanyPartnerCompaniesAPIVIew(ListAPIView):
    serializer_class = EmployerCompanySerializer

    def get_object(self):
        return get_object_or_404(InsuranceCompany, pk=self.kwargs['pk'])

    def get_queryset(self):
        insurance_company = self.get_object()
        return EmployerCompany.objects.filter(
            employees__insurance_company_id=insurance_company.id
        ).distinct()

