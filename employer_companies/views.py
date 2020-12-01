from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from users.models import EmployedUser, EmployerCompanyRepresentative
from users.serializers import EmployedUserCreateSerializer, EmployedUserSerializer
from .models import EmployerCompany
from users.serializers import EmployerCompanyRepresentativeCreateSerializer, EmployerCompanyRepresentativeSerializer
from .serializers import EmployerCompanySerializer, EmployerCompanyCoveragePriceSerializer
from .services import get_employer_company_coverage_prices


class EmployerCompanyListCreateAPIView(ListCreateAPIView):
    queryset = EmployerCompany.objects.all()
    serializer_class = EmployerCompanySerializer


class EmployerCompanyReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmployerCompany.objects.all()
    serializer_class = EmployerCompanySerializer


class EmployedUserListCreateAPIVIew(ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployedUserCreateSerializer
        return EmployedUserSerializer

    def get_queryset(self):
        employer_company = get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])
        return EmployedUser.objects.filter(employed_user_more__employer_company=employer_company)


class EmployedUserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmployedUser.objects.all()
    serializer_class = EmployedUserSerializer
    lookup_url_kwarg = 'employee_pk'


class EmployerCompanyRepresentativeListCreateAPIView(ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployerCompanyRepresentativeCreateSerializer
        return EmployerCompanyRepresentativeSerializer

    def get_queryset(self):
        employer_company = get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])
        return EmployerCompanyRepresentative.objects.filter(
            employer_company_representative_more__employer_company=employer_company
        )


class EmployerCompanyRepresentativeReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmployerCompanyRepresentativeSerializer
    lookup_url_kwarg = 'representative_pk'

    def get_queryset(self):
        employer_company = get_object_or_404(EmployerCompany, pk=self.kwargs['employer_company_pk'])
        return EmployerCompanyRepresentative.objects.filter(
            employer_company_representative_more__employer_company=employer_company
        )


class EmployerCompanyCoveragePriceListAPIView(ListAPIView):
    serializer_class = EmployerCompanyCoveragePriceSerializer

    def get_queryset(self):
        employer_company = get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])
        return get_employer_company_coverage_prices(employer_company)
