from django.contrib import admin

from library.models import Author, Book, BookSection, LibraryRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('authors',)


@admin.register(BookSection)
class BookSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(LibraryRecord)
class LibraryRecordAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'book')
