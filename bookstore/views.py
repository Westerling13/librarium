from rest_framework.generics import ListCreateAPIView

from bookstore.models import Book
from bookstore.serializers import BookListCreateSerializer


class BookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookListCreateSerializer
    queryset = Book.objects.all()
