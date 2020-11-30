from rest_framework import serializers

from .models import EmployerCompany, EmployerCompanyCoveragePrice


class EmployerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerCompany
        fields = '__all__'


class EmployerCompanyCoveragePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerCompanyCoveragePrice
        fields = '__all__'
