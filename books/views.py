import sys

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Author, Book
from .api.serializers import AuthorSerializer, BookSerializer


# used in development for rendering vue template
class IndexTemplateView(TemplateView):

    def get_template_names(self):
        RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver' or sys.argv[1] == 'process_tasks')
        print("IS RUNNING_DEVSERVER: ", RUNNING_DEVSERVER)
        if settings.DEBUG and RUNNING_DEVSERVER:
            template_name = "index-dev.html"
        else:
            template_name = "index.html"
        return template_name


# api-view for book
class BookView(APIView):
    permission_classes = (AllowAny,)  # allow any unathenticated request

    def get(self, request, pk=None):
        if pk:
            book = get_object_or_404(Book, pk=pk)
            serializer = BookSerializer(book)
            return Response({"book": serializer.data}, status=status.HTTP_200_OK)

        # No PK provided
        recent = request.query_params.get('recent') or None
        if recent:
            books = Book.objects.all().order_by('-last_updated')[:5]  # 5 books from the db sorted by last_updated
        else:
            books = Book.objects.all()

        serializer = BookSerializer(books, many=True)  # return all books
        return Response({"books": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Book Name'),
            'isbn': openapi.Schema(type=openapi.TYPE_STRING, description='Book ISBN'),
            'author_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),
        }),
        responses={200: BookSerializer, 400: 'Bad Request'})  # for documentation
    def post(self, request):
        try:

            print("request.data", request.data)
            book_name = request.data.get("name")

            # check if book is present. So as to avoid duplicates
            if Book.objects.filter(name=book_name).exists():
                print("Duplicate Book")
                return Response({"status": "error", "result": "Duplicate Book"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            # Validate book data then save
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                new_book = serializer.save()
                return Response({"status": "success", "result": serializer.data,
                                 "message": f"Book '{new_book.name}' created successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                error_dict = {}
                for field_name, field_errors in serializer.errors.items():
                    print(field_name, field_errors)
                    error_dict[field_name] = field_errors[0]
                return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"status": "error", "result": "An error occurred"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Book Name'),
            'isbn': openapi.Schema(type=openapi.TYPE_STRING, description='Book ISBN'),
            'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description='Book ID'),
            'author_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),
        }),
        responses={200: BookSerializer, 400: 'Bad Request'})  # for documentation
    def put(self, request, pk):
        book_name = request.data.get("name")

        # check if book is present. So as to avoid duplicates
        if Book.objects.filter(name=book_name).exists():
            print("Duplicate Book")
            return Response({"status": "error", "result": "Duplicate Book"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": f"Book '{book.name}' updated successfully", "result": serializer.data})
        else:
            error_dict = {}
            for field_name, field_errors in serializer.errors.items():
                print(field_name, field_errors)
                error_dict[field_name] = field_errors[0]
            return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)


class AuthorView(APIView):
    def get(self, request, pk=None):
        if pk:
            author = get_object_or_404(Author, pk=pk)
            serializer = AuthorSerializer(author)
            return Response({"author": serializer.data}, status=status.HTTP_200_OK)

        recent = request.query_params.get('recent') or None
        if recent:
            authors = Author.objects.all().order_by('-last_updated')[:3]  # 3 authors from the db sorted by last_updated
        else:
            authors = Author.objects.all()

        serializer = AuthorSerializer(authors, many=True)  # return all authors
        return Response({"authors": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Author FirstName'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Author LastName'),
        }),
        responses={200: AuthorSerializer, 400: 'Bad Request'})  # for documentation
    def post(self, request):
        try:
            print("request.data", request.data)
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")

            # check if author name is present. So as to avoid duplicates
            if Author.objects.filter(last_name=last_name, first_name=first_name).exists():
                print("Duplicate Author Name")
                return Response({"status": "error", "result": "Duplicate Author"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            # Validate author data then save
            serializer = AuthorSerializer(data=request.data)
            if serializer.is_valid():
                new_author = serializer.save()
                return Response({"status": "success", "result": serializer.data,
                                 "message": f"Author '{new_author.full_name}' created successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                error_dict = {}
                for field_name, field_errors in serializer.errors.items():
                    print(field_name, field_errors)
                    error_dict[field_name] = field_errors[0]
                return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"status": "error", "result": "An error occurred"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Author FirstName'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Author LastName'),
            'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description='Author ID'),

        }),
        responses={200: AuthorSerializer, 400: 'Bad Request'})  # for documentation
    def put(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        # check if author name is present. So as to avoid duplicates
        if Author.objects.filter(last_name=last_name, first_name=first_name).exists():
            print("Duplicate Author Name")
            return Response({"status": "error", "result": "Duplicate Author Name"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": f"Author '{author.full_name}' updated successfully",
                 "result": serializer.data})
        else:
            error_dict = {}
            for field_name, field_errors in serializer.errors.items():
                print(field_name, field_errors)
                error_dict[field_name] = field_errors[0]
            return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)
