from rest_framework import serializers

from .models import InsuranceCompany


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'
