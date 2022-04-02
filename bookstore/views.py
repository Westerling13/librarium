from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from bookstore.models import Book, Category
from bookstore.serializers import BookListCreateSerializer, BookSerializer, CategorySerializer


class BookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookListCreateSerializer
    queryset = Book.objects.all()


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
