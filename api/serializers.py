from django.contrib.auth import get_user_model
from rest_framework import serializers

from books.models import Book
from members.models import Members
from book_loans.models import BookLoans
from librarians.models import Librarians


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "email", "password", "is_staff"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "stock",
            "description",
            "cover_image",
            "category",
            "published_year",
            "created_at",
            "updated_at",
        ]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ["id", "name", "email", "password", "created_at", "updated_at"]


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarians
        fields = ["id", "name", "email", "password", "created_at", "updated_at"]


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoans
        fields = [
            "id",
            "book",
            "member",
            "librarian",
            "notes",
            "loan_date",
            "due_date",
            "return_date",
            "created_at",
            "updated_at",
        ]
