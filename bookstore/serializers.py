from rest_framework import serializers

from bookstore.models import Book, Author, BookSection


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'forename', 'surname', 'patronymic']


class BookSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSection
        fields = ['id', 'title']


class BookSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField(help_text='URL обложки')
    section = BookSectionSerializer(help_text='Книжный раздел')
    authors = AuthorSerializer(help_text='Список авторов', many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'section', 'authors', 'cover', 'free_copies_number']

    def get_cover(self, book: Book) -> str:
        return book.cover.url if book.cover.name else ''
