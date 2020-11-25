from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import EmployedUser, UnemployedUser, EmployerCompanyRepresentative, Measurement

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'role', 'job', 'insurance_company',
                  'employer_company']


class UserCreateSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.pop('confirm_password', None)

        if password != confirm_password:
            raise ValidationError(_('password and confirm_password must be equal'))

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmployedUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = EmployedUser
        fields = [f for f in UserSerializer.Meta.fields if f not in ['role', 'insurance_company']]


class EmployedUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = EmployedUser
        fields = [f for f in UserCreateSerializer.Meta.fields if f not in ['role', 'insurance_company']]

    def create(self, validated_data):
        return EmployedUser.objects.create_user(**validated_data)


class UnemployedUserSerializer(UserSerializer):
    class Meta:
        model = UnemployedUser
        fields = [f for f in UserSerializer.Meta.fields if f not in ['role', 'employer_company', 'job']]


class UnemployedUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UnemployedUser
        fields = [f for f in UserCreateSerializer.Meta.fields if f not in ['role', 'employer_company', 'job']]
        extra_kwargs = {**UserCreateSerializer.Meta.extra_kwargs, 'role': {'read_only': True}}

    def create(self, validated_data):
        return UnemployedUser.objects.create_user(**validated_data)


class EmployerCompanyRepresentativeSerializer(UserSerializer):
    class Meta:
        model = EmployerCompanyRepresentative
        fields = [f for f in UserSerializer.Meta.fields if f not in ['role', 'job', 'insurance_company']]


class EmployerCompanyRepresentativeCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = EmployerCompanyRepresentative
        fields = [f for f in UserCreateSerializer.Meta.fields if f not in ['role', 'job', 'insurance_company']]

    def create(self, validated_data):
        return EmployerCompanyRepresentative.objects.create_user(**validated_data)


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')

        if end - start < timedelta(days=1):
            raise ValidationError(_('Measurement can not last less than 1 day'))

        return attrs
