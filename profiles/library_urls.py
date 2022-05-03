from django.urls import path

from profiles.views import LibraryRecordListCreateAPIView, LibraryRecordDetailAPIView

app_name = 'library'

urlpatterns = [
    path('records/', LibraryRecordListCreateAPIView.as_view(), name='record_list_create'),
    path('records/<int:library_record_id>/', LibraryRecordDetailAPIView.as_view(), name='record_detail'),
]
