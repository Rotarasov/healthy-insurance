from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UnemployedUser, Measurement, EmployedUser
from .serializers import UnemployedUserCreateSerializer, UnemployedUserSerializer, MeasurementSerializer, \
    InsurancePriceSerializer
from .services import create_user_insurance_price, get_latest_user_insurance_price, create_company_coverage_price


User = get_user_model()


class MeasurementListCreateAPIView(ListCreateAPIView):
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Measurement.objects.filter(insurance_price__user=user)

    def perform_create(self, serializer):
        base_user = get_object_or_404(User, pk=self.kwargs['pk'])

        if base_user.role == User.Roles.EMPLOYED:
            user = EmployedUser.objects.get(pk=base_user.id)
        else:
            user = UnemployedUser.objects.get(pk=base_user.id)

        measurement = serializer.save()
        insurance_price = create_user_insurance_price(user, measurement)

        if isinstance(user, EmployedUser):
            employer_company = user.more.employer_company
            create_company_coverage_price(insurance_price, employer_company)


class MeasurementReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MeasurementSerializer
    lookup_url_kwarg = 'measurement_pk'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return Measurement.objects.filter(insurance_price__user=user)


class UnemployedUserCreateAPIVIew(ListCreateAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserCreateSerializer


class UnemployedUserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserSerializer


class GetLatestUserInsurancePrice(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        insurance_price = get_latest_user_insurance_price(user)
        serializer = InsurancePriceSerializer(instance=insurance_price)
        return Response(serializer.data)

