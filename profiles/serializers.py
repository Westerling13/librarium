from django.db.transaction import atomic
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from profiles.models import LibraryRecord
from profiles.user import User


class UserCreateSerializer(serializers.ModelSerializer):
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


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class LibraryRecordSerializer(serializers.ModelSerializer):
    class ValidationMessages:
        BOOK_IS_ALREADY_BEING_READ = 'Вы уже читаете эту книгу.'
        NO_FREE_BOOKS = 'Нет свободных экземпляров.'

    class Meta:
        model = LibraryRecord
        fields = ['id', 'book', 'status']
        extra_kwargs = {
            'book': {'write_only': True},
            'status': {'read_only': True},
        }

    def validate(self, data: dict) -> dict:
        user = self.context['request'].user
        if user.library_records.filter(book=data['book']).exists():
            raise exceptions.ValidationError(self.ValidationMessages.BOOK_IS_ALREADY_BEING_READ)

        if not data['book'].free_copies_number:
            raise exceptions.ValidationError(self.ValidationMessages.NO_FREE_BOOKS)

        data['user'] = user
        return data

    @atomic
    def create(self, validated_data: dict) -> LibraryRecord:
        reading_record = super().create(validated_data)
        validated_data['book'].free_copies_number -= 1
        validated_data['book'].save(update_fields=['free_copies_number', 'dt_updated'])
        return reading_record
