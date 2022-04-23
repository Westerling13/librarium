
from rest_framework import serializers

from bookstore.models import Book, Author, BookSection


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'forename', 'surname', 'patronymic']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'section', 'authors']


class BookSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSection
        fields = ['id', 'title']
