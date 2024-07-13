from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Role
from books.models import Book, Category
from members.models import Members
from book_loans.models import BookLoans
from librarians.models import Librarians


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = "__all__"


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarians
        fields = "__all__"


class BookLoanSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source="book", read_only=True)
    member_detail = MemberSerializer(source="member", read_only=True)
    librarian_detail = LibrarianSerializer(source="librarian", read_only=True)

    class Meta:
        model = BookLoans
        fields = "__all__"


class MemberLoanSerializer(BookLoanSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["is_overdue"] = instance.due_date.date() < datetime.now().date()
        return data

    class Meta:
        model = BookLoans
        fields = ["book", "loan_date", "due_date", "is_overdue"]
