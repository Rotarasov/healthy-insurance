from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import (
    EmployedUser,
    UnemployedUser,
    EmployerCompanyRepresentative,
    Measurement,
    EmployedUserMore,
    UnemployedUserMore,
    EmployerCompanyRepresentativeMore,
    InsurancePrice)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'role']
        extra_kwargs = {'role': {'read_only': True}}


class UserCreateSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password', 'confirm_password']
        extra_kwargs = {**UserSerializer.Meta.extra_kwargs, 'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.pop('confirm_password', None)

        if password != confirm_password:
            raise ValidationError(_('password and confirm_password must be equal'))

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmployedUserMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployedUserMore
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class EmployedUserSerializer(UserSerializer):
    employed_user_more = EmployedUserMoreSerializer(required=True)

    class Meta(UserSerializer.Meta):
        model = EmployedUser
        fields = UserSerializer.Meta.fields + ['employed_user_more']

    def update(self, instance, validated_data):
        employed_user_more_data = validated_data.pop('employed_user_more')
        for attr, value in employed_user_more_data.items():
            setattr(instance.more, attr, value)
        instance.more.save()
        return super().update(instance, validated_data)


class EmployedUserCreateSerializer(UserCreateSerializer):
    employed_user_more = EmployedUserMoreSerializer(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = EmployedUser
        fields = UserCreateSerializer.Meta.fields + ['employed_user_more']

    def create(self, validated_data):
        employed_user_more_data = validated_data.pop('employed_user_more')
        employed_user = EmployedUser.objects.create_user(**validated_data)
        EmployedUserMore.objects.create(user=employed_user, **employed_user_more_data)
        return employed_user


class UnemployedUserMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnemployedUserMore
        exclude = ['user']


class UnemployedUserSerializer(UserSerializer):
    unemployed_user_more = UnemployedUserMoreSerializer(required=True)

    class Meta(UserSerializer.Meta):
        model = UnemployedUser
        fields = UserSerializer.Meta.fields + ['unemployed_user_more']

    def update(self, instance, validated_data):
        unemployed_user_more_data = validated_data.pop('unemployed_user_more')
        for attr, value in unemployed_user_more_data.items():
            setattr(instance.more, attr, value)
        instance.more.save()
        return super().update(instance, validated_data)


class UnemployedUserCreateSerializer(UserCreateSerializer):
    unemployed_user_more = UnemployedUserMoreSerializer(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = UnemployedUser
        fields = UserCreateSerializer.Meta.fields + ['unemployed_user_more']

    def create(self, validated_data):
        unemployed_user_more_data = validated_data.pop('unemployed_user_more')
        unemployed_user = UnemployedUser.objects.create_user(**validated_data)
        UnemployedUserMore.objects.create(user=unemployed_user, **unemployed_user_more_data)
        return unemployed_user


class EmployerCompanyRepresentativeMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerCompanyRepresentativeMore
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class EmployerCompanyRepresentativeSerializer(UserSerializer):
    employer_company_representative_more = EmployerCompanyRepresentativeMoreSerializer(required=True)

    class Meta(UserSerializer.Meta):
        model = EmployerCompanyRepresentative
        fields = UserSerializer.Meta.fields + ['employer_company_representative_more']

    def update(self, instance, validated_data):
        employer_company_representative_more_data = validated_data.pop('employer_company_representative_more', {})
        for attr, value in employer_company_representative_more_data.items():
            setattr(instance.more, attr, value)
        instance.more.save()
        return super().update(instance, validated_data)


class EmployerCompanyRepresentativeCreateSerializer(UserCreateSerializer):
    employer_company_representative_more = EmployerCompanyRepresentativeMoreSerializer(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = EmployerCompanyRepresentative
        fields = UserCreateSerializer.Meta.fields + ['employer_company_representative_more']

    def create(self, validated_data):
        employer_company_representative_more_data = validated_data.pop('employer_company_representative_more')
        employer_company_representative = EmployerCompanyRepresentative.objects.create_user(**validated_data)
        EmployerCompanyRepresentativeMore.objects.create(user=employer_company_representative,
                                                         **employer_company_representative_more_data)
        return employer_company_representative


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


class InsurancePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePrice
        fields = '__all__'
