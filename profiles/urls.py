from django.urls import path

from profiles.views import ProfileLibraryRecordListAPIView

app_name = 'profile'

urlpatterns = [
    path('books/', ProfileLibraryRecordListAPIView.as_view(), name='profile_library_record_list'),
]
