from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from bookstore.models import Book
from bookstore.serializers import BookListCreateSerializer, BookSerializer


class BookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookListCreateSerializer
    queryset = Book.objects.all()


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'
