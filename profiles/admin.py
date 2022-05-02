from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from profiles.models import Profile, LibraryRecord
from profiles.user import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


@admin.register(LibraryRecord)
class BookReadingRecordAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'book')
