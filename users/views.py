from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .serializers import UserSerializer, UserCreateSerializer, UserUpdatePasswordSerializer


User = get_user_model()


@api_view(http_method_names=['PUT'])
# @permission_classes([IsAuthenticated])
def update_user_password(request, *args, **kwargs):
    serializer = UserUpdatePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user_serializer = UserSerializer(serializer.save())
    return Response(user_serializer.data)


class UserCreateAPIVIew(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

