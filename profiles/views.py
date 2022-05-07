from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from library.models import LibraryRecord
from profiles.serializers import ProfileLibraryRecordSerializer


class ProfileLibraryRecordListAPIView(ListCreateAPIView):
    serializer_class = ProfileLibraryRecordSerializer

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        status = self.request.query_params.get('status')
        if not status:
            return queryset

        return queryset.filter(status=status)

    def get_queryset(self) -> QuerySet:
        return LibraryRecord.objects.filter(user=self.request.user).select_related('book')

    @extend_schema(summary='Список взятых книг')
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Список взятых книг."""
        return self.list(request, *args, **kwargs)


class ProfileLibraryRecordDetailAPIView(GenericAPIView, UpdateModelMixin):
    serializer_class = ProfileLibraryRecordSerializer
    lookup_url_kwarg = 'book_id'
    lookup_field = 'book_id'

    def get_object(self):
        return get_object_or_404(LibraryRecord, status=LibraryRecord.READING, book_id=self.kwargs['book_id'])

    @extend_schema(summary='Вернуть книгу')
    def post(self, request, *args, **kwargs):
        """Вернуть книгу, если она находится в процессе чтения."""
        return self.update(request, *args, **kwargs)
