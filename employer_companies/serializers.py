from rest_framework import serializers

from .models import EmployerCompany


class EmployerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerCompany
        fields = '__all__'
