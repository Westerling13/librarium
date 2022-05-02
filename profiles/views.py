from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from profiles.models import LibraryRecord
from profiles.serializers import LibraryRecordSerializer


class LibraryRecordListCreateAPIView(ListCreateAPIView):
    serializer_class = LibraryRecordSerializer

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
