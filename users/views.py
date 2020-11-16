from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView

from .serializers import UserSerializer, UserCreateUpdateSerializer

User = get_user_model()


class UserCreateAPIVIew(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

