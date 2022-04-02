from django.urls import path

from bookstore.views import BookListCreateAPIView, BookDetailAPIView

appname = 'bookstore'

urlpatterns = [
    path('', BookListCreateAPIView.as_view(), name='list'),
    path('<int:book_id>/', BookDetailAPIView.as_view(), name='detail'),
]
