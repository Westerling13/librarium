from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bookstore.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['forename', 'surname', 'patronymic', 'short_name']
        extra_kwargs = {
            'forename': {'write_only': True},
            'surname': {'write_only': True},
            'patronymic': {'write_only': True},
            'short_name': {'read_only': True},
        }


class BookListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'dt_release']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(help_text='ФИО автора')

    class Meta:
        model = Book
        fields = ['title', 'author']

    def get_author_name(self, book):
        return book.author.short_name
