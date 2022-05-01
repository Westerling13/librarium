from rest_framework import serializers, exceptions

from bookstore.models import Book, Author, BookSection, BookReadingRecord


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'forename', 'surname', 'patronymic']


class BookSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSection
        fields = ['number', 'title']


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


class BookReadingRecordSerializer(serializers.ModelSerializer):
    class ValidationMessages:
        BOOK_IS_ALREADY_BEING_READ = 'Вы уже читаете эту книгу.'
        NO_FREE_BOOKS = 'Нет свободных экземпляров.'

    class Meta:
        model = BookReadingRecord
        fields = []

    def validate(self, data: dict) -> dict:
        book, user = self.context['book'], self.context['request'].user
        if user.book_reading_records.filter(book=book).exists():
            raise exceptions.ValidationError(self.ValidationMessages.BOOK_IS_ALREADY_BEING_READ)

        if not book.free_copies_number:
            raise exceptions.ValidationError(self.ValidationMessages.NO_FREE_BOOKS)

        data['book'] = book
        data['user'] = user

        return data
