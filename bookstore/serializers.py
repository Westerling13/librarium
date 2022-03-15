from rest_framework import serializers

from bookstore.models import Book


class BookListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(help_text='ФИО автора')

    class Meta:
        model = Book
        fields = ['title', 'author']

    def get_author_name(self, book):
        return book.author.short_name
