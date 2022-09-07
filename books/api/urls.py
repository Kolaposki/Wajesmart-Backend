from django.contrib import admin
from django.urls import path, include, re_path
from books.views import BookView, AuthorView

urlpatterns = [
    # Authors
    path("authors/", AuthorView.as_view(), name="authors"),
    path("author/", AuthorView.as_view(), name="new_author"),
    path("author/<int:pk>", AuthorView.as_view(), name="author"),

    # Books
    path("books/", BookView.as_view(), name="books"),
    path("book/", BookView.as_view(), name="new_book"),
    path("book/<int:pk>", BookView.as_view(), name="book"),
]
