from typing import Type

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from library.models import Book, BookSection
from library.serializers import BookSerializer, BookDetailSerializer, BookOperateSerializer, BookSectionSerializer


class BookDetailAPIView(RetrieveAPIView, UpdateModelMixin):
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.request.method == 'GET':
            return BookDetailSerializer

        return BookOperateSerializer

    @extend_schema(summary="Взять книгу", request=None)
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Взять книгу, если она еще не на руках и есть в наличии, иначе будет соответствующая ошибка."""
        return self.update(request, *args, **kwargs)


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('section__number', 'title')

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        section_key = self.request.query_params.get('section')
        if not section_key:
            return queryset

        return queryset.filter(section__key=section_key)

    @extend_schema(summary='Список книг')
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Список книг."""
        return self.list(request, *args, **kwargs)


class BookSectionListAPIView(ListAPIView):
    serializer_class = BookSectionSerializer
    queryset = BookSection.objects.all()

    @extend_schema(summary='Список разделов')
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Список книжных разделов."""
        return self.list(request, *args, **kwargs)
