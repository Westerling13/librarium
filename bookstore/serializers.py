
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
    section = BookSectionSerializer()
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'section', 'authors', 'cover', 'free_copies_number']
