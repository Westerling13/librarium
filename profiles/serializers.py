from typing import List

from django.db.transaction import atomic
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from bookstore.models import Book
from bookstore.serializers import BookSectionSerializer, AuthorSerializer
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
    book_id = serializers.IntegerField()
    title = serializers.CharField(source='book__title', read_only=True)
    section = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField(help_text='URL обложки')
    authors = serializers.SerializerMethodField()

    class ValidationMessages:
        BOOK_IS_ALREADY_BEING_READ = 'Вы уже читаете эту книгу.'
        NO_FREE_BOOKS = 'Нет свободных экземпляров.'

    class Meta:
        model = LibraryRecord
        fields = ['id', 'book_id', 'status', 'title', 'section', 'cover', 'authors', 'dt_return']
        extra_kwargs = {
            'status': {'read_only': True},
            'dt_return': {'read_only': True},
        }

    def get_cover(self, library_record: LibraryRecord) -> str:
        return library_record.book.cover.url if library_record.book.cover.name else ''

    def get_section(self, library_record: LibraryRecord):
        return BookSectionSerializer(library_record.book.section).data

    def get_authors(self, library_record: LibraryRecord) -> List[dict]:
        return AuthorSerializer(library_record.book.authors, many=True).data

    def validate(self, data: dict) -> dict:
        user = self.context['request'].user
        if user.library_records.filter(book_id=data['book_id'], status=LibraryRecord.READING).exists():
            raise exceptions.ValidationError(self.ValidationMessages.BOOK_IS_ALREADY_BEING_READ)

        book = get_object_or_404(Book, id=data['book_id'])
        if not book.free_copies_number:
            raise exceptions.ValidationError(self.ValidationMessages.NO_FREE_BOOKS)

        data['book'] = book
        data['user'] = user
        return data

    @atomic
    def create(self, validated_data: dict) -> LibraryRecord:
        book = validated_data.pop('book')
        library_record = super().create(validated_data)
        book.free_copies_number -= 1
        book.save(update_fields=['free_copies_number', 'dt_updated'])
        return library_record
