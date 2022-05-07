from typing import List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import LibraryRecord
from library.serializers import AuthorSerializer
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


class ProfileLibraryRecordSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(help_text='ID книги')
    cover = serializers.SerializerMethodField(help_text='Обложка книги')
    title = serializers.SerializerMethodField(help_text='Название книги')
    authors = serializers.SerializerMethodField(help_text='Авторы книги')

    class Meta:
        model = LibraryRecord
        fields = ['status', 'dt_return', 'id', 'cover', 'title', 'authors']

    def get_id(self, library_record: LibraryRecord) -> int:
        return library_record.book.id

    def get_cover(self, library_record: LibraryRecord) -> str:
        return library_record.book.cover.url if library_record.book.cover.name else ''

    def get_title(self, library_record: LibraryRecord) -> str:
        return library_record.book.title

    def get_authors(self, library_record: LibraryRecord) -> List[dict]:
        return AuthorSerializer(library_record.book.authors, many=True).data
