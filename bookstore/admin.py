from django.contrib import admin

from bookstore.models import Author, Book, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
