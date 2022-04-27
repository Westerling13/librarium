from django.urls import path

from profiles.views import UsersRegisterAPIView, UsersLoginAPIView, UsersLogoutAPIView, CheckAPIView

urlpatterns = [
    path('register/', UsersRegisterAPIView.as_view(), name='register'),
    path('login/', UsersLoginAPIView.as_view(), name='login'),
    path('logout/', UsersLogoutAPIView.as_view(), name='logout'),
    path('check/', CheckAPIView.as_view(), name='check'),
]
