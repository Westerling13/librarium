from django.db.transaction import atomic
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
    authors = serializers.ListField(child=AuthorSerializer(), write_only=True, allow_null=True)
    authors_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, allow_null=True)
    authors_names = serializers.SerializerMethodField()

    EMPTY_AUTHORS_VALIDATION_MESSAGE = 'У книги должны быть указаны авторы.'

    class Meta:
        model = Book
        fields = ['id', 'title', 'dt_release', 'authors', 'authors_names', 'authors_ids']

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

    def get_authors_names(self, book):
        return book.authors.short_names()


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'authors']
