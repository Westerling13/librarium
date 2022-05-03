from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from profiles.models import LibraryRecord
from profiles.serializers import LibraryRecordSerializer


class LibraryRecordListCreateAPIView(ListCreateAPIView):
    serializer_class = LibraryRecordSerializer
    filter_backends = [SearchFilter]
    search_fields = ['=status', 'book__title']

    def get_queryset(self):
        return LibraryRecord.objects.filter(user=self.request.user).select_related('book').order_by('dt_created')

    @extend_schema(summary='Список книг пользователя')
    def get(self, request, *args, **kwargs):
        """По умолчанию возвращается список книг, находящихся в процессе прочтения."""
        return self.list(request, *args, **kwargs)

    @extend_schema(summary='Взять книгу')
    def post(self, request, *args, **kwargs):
        """Взять книгу."""
        return self.create(request, *args, **kwargs)


class LibraryRecordDetailAPIView(GenericAPIView):
    lookup_url_kwarg = 'library_record_id'

    def get_queryset(self):
        return LibraryRecord.objects.filter(user=self.request.user)

    @extend_schema(summary='Вернуть книги', responses={
        status.HTTP_204_NO_CONTENT: None,
    })
    def post(self, request, *args, **kwargs):
        """Вернуть книгу."""
        library_record = self.get_object()
        library_record.return_book()

        return Response(status=status.HTTP_204_NO_CONTENT)
