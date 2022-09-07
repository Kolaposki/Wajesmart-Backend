from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Book, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'isbn', 'author', 'created_at',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_per_page = 50


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'created_at',)
    list_display_links = ('id', 'first_name',)
    search_fields = ('first_name',)
    list_per_page = 50


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.unregister(Group)  # remove Group objects from admin page:  under[Authentication and Authorization]
