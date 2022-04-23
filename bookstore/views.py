from rest_framework.generics import RetrieveAPIView, ListAPIView

from bookstore.models import Book
from bookstore.serializers import BookSerializer


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
