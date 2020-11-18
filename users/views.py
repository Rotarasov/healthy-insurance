from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import UserSerializer, UserCreateSerializer


User = get_user_model()


class UserCreateAPIVIew(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

