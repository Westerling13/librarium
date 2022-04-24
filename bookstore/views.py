from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView

from bookstore.models import Book
from bookstore.serializers import BookSerializer


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('section__number', 'title')

    @extend_schema(summary='Список книг')
    def get(self, request, *args, **kwargs):
        """Список книг"""
        return self.list(request, *args, **kwargs)
