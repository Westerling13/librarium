from django.contrib import admin

from bookshelves.models import UserBook


@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'book')
