from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bookstore.models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'forename', 'surname', 'patronymic']


class BookListCreateSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    authors_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, allow_null=True)

    EMPTY_AUTHORS_VALIDATION_MESSAGE = 'У книги должны быть указаны авторы.'

    class Meta:
        model = Book
        fields = ['id', 'title', 'dt_release', 'authors', 'authors_ids']

    def validate(self, attrs):
        if not attrs['authors'] and not attrs['authors_ids']:
            raise ValidationError(self.EMPTY_AUTHORS_VALIDATION_MESSAGE)

        return attrs

    @atomic
    def create(self, validated_data):
        authors = [Author.objects.create(**author) for author in validated_data.pop('authors')]
        authors.extend(list(Author.objects.filter(id__in=validated_data.pop('authors_ids'))))
        book = super().create(validated_data)
        book.authors.add(*authors)
        return book


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'authors']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
