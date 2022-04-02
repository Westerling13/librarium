from django.urls import path

from bookstore.views import BookListCreateAPIView, BookDetailAPIView

appname = 'bookstore'

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book_list'),
    path('books/<int:book_id>/', BookDetailAPIView.as_view(), name='book_detail'),
]
