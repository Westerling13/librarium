from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import Book, Author, BookSection, LibraryRecord


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'forename', 'surname', 'patronymic']


class BookSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSection
        fields = ['number', 'key', 'title']


class BookSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField(help_text='URL обложки')
    is_available = serializers.SerializerMethodField(help_text='Книга доступна')
    section = BookSectionSerializer(help_text='Книжный раздел')
    authors = AuthorSerializer(help_text='Список авторов', many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'section', 'authors', 'cover', 'is_available']

    def get_cover(self, book: Book) -> str:
        return book.cover.url if book.cover.name else ''

    def get_is_available(self, book: Book) -> bool:
        return bool(book.free_copies_number)


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'section', 'description', 'authors', 'cover', 'is_available', 'edition', 'publication_year',
        ]


class BookOperateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = []

    BOOK_ALREADY_READING_VALIDATION_MESSAGE = 'Вы уже читаете эту книгу.'
    NO_FREE_BOOKS_VALIDATION_MESSAGE = 'Нет свободных экземпляров.'

    def validate(self, data):
        if self.instance.library_records.filter(
            user=self.context['request'].user, status=LibraryRecord.READING,
        ).exists():
            raise ValidationError(self.BOOK_ALREADY_READING_VALIDATION_MESSAGE)

        if not self.instance.free_copies_number:
            raise ValidationError(self.NO_FREE_BOOKS_VALIDATION_MESSAGE)

        return data

    @atomic
    def update(self, instance: Book, validated_data: dict) -> Book:
        user = self.context['request'].user
        instance.library_records.create(user=user)
        instance.free_copies_number -= 1
        instance.save(update_fields=['free_copies_number', 'dt_updated'])
        return instance
