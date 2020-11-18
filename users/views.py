from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import UnemployedUser, EmployerCompanyRepresentative
from .serializers import (
    UnemployedUserCreateSerializer,
    UnemployedUserSerializer,
    EmployerCompanyRepresentativeSerializer,
    EmployerCompanyRepresentativeCreateSerializer
)

User = get_user_model()


class UnemployedUserCreateAPIVIew(CreateAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserCreateSerializer


class UnemployedUserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserSerializer


class EmployerCompanyRepresentativeCreateAPIView(CreateAPIView):
    queryset = EmployerCompanyRepresentative.objects.all()
    serializer_class = EmployerCompanyRepresentativeCreateSerializer


class EmployerCompanyRepresentativeReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmployerCompanyRepresentative.objects.all()
    serializer_class = EmployerCompanyRepresentativeSerializer

