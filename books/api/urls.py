from django.contrib import admin
from django.urls import path, include, re_path
from books.views import BookView


urlpatterns = [
    # Authors
    # path("authors/", AuthorView.as_view()),
    # path("author/<int:pk>", AuthorView.as_view()),

    # Books
    path("books/", BookView.as_view(), name="books"),
    path("book/<int:pk>", BookView.as_view(), name="book"),
]
