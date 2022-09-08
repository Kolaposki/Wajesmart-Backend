import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from .api.serializers import AuthorSerializer, BookSerializer

from .models import Author, Book

client = Client()


class GetAllBookTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            first_name="Mark",
            last_name="Zuck",
        )
        self.author2 = Author.objects.create(
            first_name="Mark",
            last_name="Zuck",
        )

        Book.objects.create(
            title="TestTitle1", author_id=self.author1.id, isbn="1-234-454"
        )
        Book.objects.create(
            title="TestTitle2", author_id=self.author2.id, isbn="1-234-454-5"
        )

    def test_get_all_books(self):
        response = self.client.get(reverse("books_api:books"))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        books_data = serializer.data
        self.assertEqual(response.data, books_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateBookTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Mark",
            last_name="Zuck",
        )

        self.valid_payload = {
            "title": "Booktest",
            "author_id": self.author.id,
            "isbn": "12-234-45",
        }
        self.invalid_payload = {
            "title": "",
            "author_id": self.author.id,
            "isbn": "12-234-453",
        }

    def test_create_book(self):
        response_book = client.post(
            reverse("books_api:books"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response_book.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response_book = client.post(
            reverse("books_api:books"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response_book.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateBookTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            first_name="Mark",
            last_name="Zuck",
        )

        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Zuck",
        )

        Book.objects.create(
            title="TestTitle1", author_id=self.author1.id, isbn="3-763-32"
        )
        Book.objects.create(
            title="TestTitle2", author_id=self.author2.id, isbn="5-0987-34"
        )
        self.valid_payload = {
            "title": "Booktest",
            "author_id": self.author1.id,
            "isbn": "12-234-",
        }
        self.invalid_payload = {
            "title": "",
            "author_id": self.author2.id,
            "isbn": "9-453-453",
        }

    def test_valid_book_update(self):
        response = self.client.put(
            reverse("books_api:book.id", kwargs={"pk": self.author1.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_book_update(self):
        response = self.client.put(
            reverse("books_api:book.id", kwargs={"pk": self.author1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllAuthorTestCase(TestCase):
    def setUp(self):
        self.valid_payload = {
            "first_name": "Mark",
            "last_name": "Zuck",
        }
        self.invalid_payload = {
            "first_name": "",
            "last_name": 1,
        }

    def test_get_all_authors(self):
        response = self.client.get(reverse("books_api:authors"))
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        authors_data = serializer.data
        self.assertEqual(response.data, authors_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateAuthorTestCase(TestCase):
    def setUp(self):
        self.valid_payload = {
            "first_name": "Mark",
            "last_name": "Zuck",
        }
        self.invalid_payload = {
            "first_name": "",
            "last_name": 1,
        }

    def test_create_valid_author(self):
        response_author = client.post(
            reverse("books_api:authors"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response_author.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response_author = client.post(
            reverse("books_api:authors"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response_author.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateAuthorTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            first_name="Mark",
            last_name="Zuck",
        )

        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Zuck",
        )

        self.valid_payload = {
            "first_name": "Mark",
            "last_name": "Zuck",
        }
        self.invalid_payload = {
            "first_name": "",
            "last_name": 1,
        }

    def test_valid_author_update(self):
        response = self.client.put(
            reverse("books_api:author.id", kwargs={"pk": self.author1.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_author_update(self):
        response = self.client.put(
            reverse("books_api:author.id", kwargs={"pk": self.author2.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
