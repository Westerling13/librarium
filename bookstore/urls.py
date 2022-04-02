from django.urls import path

from bookstore.views import BookListCreateAPIView, BookDetailAPIView, CategoryListCreateAPIView

appname = 'bookstore'

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book_list'),
    path('books/<int:book_id>/', BookDetailAPIView.as_view(), name='book_detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category_list'),
]
