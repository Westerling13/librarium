from django.contrib.auth import login, authenticate, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.serializers import UsersCreateSerializer, UsersLoginSerializer


class UsersRegisterAPIView(GenericAPIView):
    serializer_class = UsersCreateSerializer
    permission_classes = [~IsAuthenticated]

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


class UsersLoginAPIView(GenericAPIView):
    serializer_class = UsersLoginSerializer
    permission_classes = [~IsAuthenticated]

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


class UsersLogoutAPIView(APIView):
    @extend_schema(request=None, summary='Логаут', responses={
        status.HTTP_204_NO_CONTENT: None,
    })
    def post(self, request, *args, **kwargs):
        """Логаут пользователя"""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersLoginSerializer

    @extend_schema(request=None, summary='Проверка авторизации', responses={
        status.HTTP_200_OK: UsersLoginSerializer,
    })
    def get(self, request, *args, **kwargs):
        """Проверка авторизации пользователя"""
        return Response({'user': request.user.username})
