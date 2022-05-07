from django.urls import path

from library.views import BookDetailAPIView, BookListAPIView

appname = 'library'

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book_list'),
    path('books/<int:book_id>/', BookDetailAPIView.as_view(), name='book_detail'),
]
