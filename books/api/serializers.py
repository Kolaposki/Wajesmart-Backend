from rest_framework import serializers

from books.models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField()

    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
