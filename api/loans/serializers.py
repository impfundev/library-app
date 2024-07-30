from django.utils import timezone
from rest_framework import serializers

from loans.models import BookLoan
from ..book.serializers import BookSerializer
from ..auth.serializers import MemberSerializer


class BookLoanSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source="book", read_only=True)
    member_detail = MemberSerializer(source="member", read_only=True)
    remaining_loan_time = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        remaining_loan_time = timezone.now().day - instance.due_date.day
        data["remaining_loan_time"] = str(remaining_loan_time) + " days left"
        return data

    class Meta:
        model = BookLoan
        fields = "__all__"


class MemberLoanSerializer(BookLoanSerializer):
    book_detail = BookSerializer(source="book", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["is_overdue"] = instance.due_date < timezone.now()
        return data

    class Meta:
        model = BookLoan
        fields = [
            "book",
            "book_detail",
            "member",
            "loan_date",
            "due_date",
            "is_overdue",
        ]
