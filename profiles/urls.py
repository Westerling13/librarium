from django.urls import path

from profiles.views import ProfileLibraryRecordListAPIView, ProfileLibraryRecordDetailAPIView

app_name = 'profile'

urlpatterns = [
    path('books/', ProfileLibraryRecordListAPIView.as_view(), name='profile_library_record_list'),
    path('books/<int:book_id>/', ProfileLibraryRecordDetailAPIView.as_view(), name='profile_library_record_detail'),
]
