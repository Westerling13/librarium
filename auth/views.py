from django.contrib.auth import login, authenticate, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import UserCreateSerializer, UserLoginSerializer


class RegistrationAPIView(GenericAPIView):
    serializer_class = UserCreateSerializer

    @extend_schema(summary='Регистрация', responses={
        status.HTTP_201_CREATED: None,
    })
    def post(self, request, *args, **kwargs):
        """Регистрация пользователя"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(summary='Логин', responses={
        status.HTTP_204_NO_CONTENT: None,
    })
    def post(self, request, *args, **kwargs):
        """Авторизация пользователя"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)
        if user is not None:
            login(request, user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutAPIView(APIView):
    @extend_schema(request=None, summary='Логаут', responses={
        status.HTTP_204_NO_CONTENT: None,
    })
    def post(self, request, *args, **kwargs):
        """Логаут пользователя"""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
