from django.urls import path

from bookstore.views import BookListCreateAPIView

appname = 'bookstore'

urlpatterns = [
    path('', BookListCreateAPIView.as_view(), name='list'),
]
