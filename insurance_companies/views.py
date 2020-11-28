from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404

from employer_companies.models import EmployerCompany
from employer_companies.serializers import EmployerCompanySerializer
from users.models import EmployedUser
from users.serializers import UnemployedUserSerializer, EmployedUserSerializer
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
    serializer_class = UnemployedUserSerializer

    def get_queryset(self):
        insurance_company = get_object_or_404(InsuranceCompany, pk=self.kwargs['pk'])
        return insurance_company.clients


class InsuranceCompanyPartnerCompaniesAPIVIew(ListAPIView):
    serializer_class = EmployerCompanySerializer

    def get_queryset(self):
        insurance_company = get_object_or_404(InsuranceCompany, pk=self.kwargs['pk'])
        return insurance_company.partner_companies

