from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UnemployedUser
from .serializers import UnemployedUserCreateSerializer, UnemployedUserSerializer
from .services import calculate_user_insurance_price


User = get_user_model()


class GetUserInsurancePrice(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        new_price = calculate_user_insurance_price(user)
        return Response({'price': new_price})


class UnemployedUserCreateAPIVIew(CreateAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserCreateSerializer


class UnemployedUserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UnemployedUser.objects.all()
    serializer_class = UnemployedUserSerializer

