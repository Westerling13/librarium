from django.contrib import admin

from bookstore.models import Author, Book, BookSection, BookReadingRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('authors',)


@admin.register(BookSection)
class BookSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(BookReadingRecord)
class BookReadingRecordAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'book')
