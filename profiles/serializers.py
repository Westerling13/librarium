import datetime
from typing import List

from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import LibraryRecord
from library.serializers import AuthorSerializer, BookSectionSerializer
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
    is_available = serializers.SerializerMethodField(help_text='Книга доступна для взятия')
    section = serializers.SerializerMethodField(help_text='Книжный раздел')

    class Meta:
        model = LibraryRecord
        fields = ['status', 'dt_return', 'id', 'cover', 'title', 'authors', 'is_available', 'section']
        extra_kwargs = {
            'id': {'read_only': True},
            'dt_return': {'read_only': True},
            'status': {'read_only': True},
        }

    def get_id(self, library_record: LibraryRecord) -> int:
        return library_record.book.id

    def get_cover(self, library_record: LibraryRecord) -> str:
        return library_record.book.cover.url if library_record.book.cover.name else ''

    def get_title(self, library_record: LibraryRecord) -> str:
        return library_record.book.title

    def get_authors(self, library_record: LibraryRecord) -> List[dict]:
        return AuthorSerializer(library_record.book.authors, many=True).data

    def get_is_available(self, library_record: LibraryRecord) -> bool:
        return bool(library_record.book.free_copies_number)

    def get_section(self, library_record: LibraryRecord) -> dict:
        return BookSectionSerializer(library_record.book.section).data

    @atomic
    def update(self, instance: LibraryRecord, validated_data: dict) -> LibraryRecord:
        instance.status = LibraryRecord.FINISHED
        instance.dt_return = datetime.datetime.now().date()
        instance.book.free_copies_number += 1
        instance.save(update_fields=['status', 'dt_updated', 'dt_return'])
        instance.book.save(update_fields=['free_copies_number', 'dt_updated'])

        return instance
