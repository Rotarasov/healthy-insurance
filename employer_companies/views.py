from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import EmployedUser, EmployerCompanyRepresentative
from users.serializers import EmployedUserCreateSerializer, EmployedUserSerializer
from .models import EmployerCompany
from users.serializers import EmployerCompanyRepresentativeCreateSerializer, EmployerCompanyRepresentativeSerializer
from .serializers import (
    EmployerCompanySerializer,
    EmployerCompanyCoveragePriceSerializer,
    EmployerCompanyPriceSerializer
)
from .services import get_employer_company_coverage_prices, get_employer_company_prices, \
    get_or_create_latest_employer_company_price


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


class EmployerCompanyPriceCreate(CreateAPIView):
    serializer_class = EmployerCompanyPriceSerializer

    def get_queryset(self):
        employer_company = get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])
        return get_employer_company_prices(employer_company)

    def create(self, request, *args, **kwargs):
        employer_company = get_object_or_404(EmployerCompany, pk=self.kwargs['pk'])
        employer_company_price = get_or_create_latest_employer_company_price(employer_company)
        serializer = self.get_serializer(instance=employer_company_price)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
