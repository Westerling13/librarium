from django.urls import path

from bookstore.views import BookDetailAPIView, BookListAPIView, BookReadingRecordCreateAPIView

appname = 'bookstore'

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book_list'),
    path('books/<int:book_id>/', BookDetailAPIView.as_view(), name='book_detail'),
    path(
        'books/<int:book_id>/reading_records/',
        BookReadingRecordCreateAPIView.as_view(),
        name='book_reading_record_create',
    ),
]
