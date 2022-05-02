from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from profiles.models import LibraryRecord
from profiles.serializers import LibraryRecordSerializer


class LibraryRecordListCreateAPIView(CreateAPIView):
    serializer_class = LibraryRecordSerializer
    queryset = LibraryRecord.objects.all()

    @extend_schema(summary='Взять книгу')
    def post(self, request, *args, **kwargs):
        """Взять книгу."""
        return self.create(request, *args, **kwargs)
