from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404

from .models import UnemployedUser, Measurement, EmployedUser
from .serializers import UnemployedUserCreateSerializer, UnemployedUserSerializer, MeasurementSerializer
from .services import create_user_insurance_price


User = get_user_model()


class MeasurementListCreateAPIView(CreateAPIView):
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
        create_user_insurance_price(user, measurement)


class MeasurementReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MeasurementSerializer
    lookup_url_kwarg = 'measurement_pk'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return Measurement.objects.filter(insurance_price__user=user)


class UnemployedUserCreateAPIVIew(CreateAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserCreateSerializer


class UnemployedUserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserSerializer

