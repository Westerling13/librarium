from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView

from bookstore.models import Book
from bookstore.serializers import BookSerializer, BookDetailSerializer, BookReadingRecordSerializer


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('section__number', 'title')

    @extend_schema(summary='Список книг')
    def get(self, request, *args, **kwargs):
        """Список книг"""
        return self.list(request, *args, **kwargs)


class BookReadingRecordCreateAPIView(CreateAPIView):
    serializer_class = BookReadingRecordSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['book'] = self.get_object()
        return context

    @extend_schema(summary='Взять книгу')
    def post(self, request, *args, **kwargs):
        """Взять книгу."""
        return self.create(request, *args, **kwargs)
