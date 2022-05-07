from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.mixins import UpdateModelMixin

from library.models import Book, BookSection
from library.serializers import BookSerializer, BookDetailSerializer, BookOperateSerializer, BookSectionSerializer


class BookDetailAPIView(RetrieveAPIView, UpdateModelMixin):
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookDetailSerializer

        return BookOperateSerializer

    @extend_schema(summary="Взять книгу", request=None)
    def post(self, request, *args, **kwargs):
        """Взять книгу, если она еще не на руках и есть в наличии, иначе будет соответствующая ошибка."""
        return self.update(request, *args, **kwargs)


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('section__number', 'title')

    @extend_schema(summary='Список книг')
    def get(self, request, *args, **kwargs):
        """Список книг."""
        return self.list(request, *args, **kwargs)


class BookSectionListAPIView(ListAPIView):
    serializer_class = BookSectionSerializer
    queryset = BookSection.objects.all()

    @extend_schema(summary='Список разделов')
    def get(self, request, *args, **kwargs):
        """Список книжных разделов."""
        return self.list(request, *args, **kwargs)
