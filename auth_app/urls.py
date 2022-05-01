from django.urls import path

from auth_app.views import RegistrationAPIView, LoginAPIView, LogoutAPIView, CsrfTokenRetrieveAPIView

app_name = 'auth_app'

urlpatterns = [
    path('', CsrfTokenRetrieveAPIView.as_view(), name='csrf_token_retrieve'),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
