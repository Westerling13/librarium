from django.urls import path

from auth.views import RegistrationAPIView, LoginAPIView, LogoutAPIView

app_name = 'auth'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registrations'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]