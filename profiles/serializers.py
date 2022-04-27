from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from profiles.user import User


class UsersCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, data):
        password, password2 = data['password'], data['password2']
        if password != password2:
            raise ValidationError('Введенные пароли не совпадают.')

        data.pop('password2')
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UsersLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
