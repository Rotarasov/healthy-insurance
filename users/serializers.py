from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'job']


class UserCreateUpdateSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.pop('confirm_password', None)

        if not password or password != confirm_password:
            raise ValidationError(_('password and confirm_password must be equal'))

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
