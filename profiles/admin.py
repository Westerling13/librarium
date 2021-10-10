from django.contrib import admin

from profiles.models import Profile
from profiles.user import User


@admin.register(User, Profile)
class UserAdmin(admin.ModelAdmin):
    """Административный класс для модели Пользователя"""
