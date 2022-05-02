from django.urls import path

from bookstore.views import BookDetailAPIView, BookListAPIView

appname = 'bookstore'

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book_list'),
    path('books/<int:book_id>/', BookDetailAPIView.as_view(), name='book_detail'),
]
