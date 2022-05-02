from django.urls import path

from profiles.views import LibraryRecordListCreateAPIView

app_name = 'library'

urlpatterns = [
    path('records/', LibraryRecordListCreateAPIView.as_view(), name='record_list_create'),
]
