from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

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
    serializer_class = InsuranceCompanySerializer

    def get_queryset(self):
        insurance_company = self.get_object()
        return User.objects.filter(insurance_company_id=insurance_company.id)


class InsuranceCompanyPartnerCompaniesAPIVIew(ListAPIView):
    serializer_class = InsuranceCompanySerializer

    # def get_queryset(self):
    #     insurance_company = self.get_object()
    #     return

