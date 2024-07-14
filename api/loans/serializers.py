from django.utils import timezone
from rest_framework import serializers

from loans.models import BookLoan
from ..book.serializers import BookSerializer
from ..auth.serializers import MemberSerializer


class BookLoanSerializer(serializers.ModelSerializer):
    book_detail = BookSerializer(source="book", read_only=True)
    member_detail = MemberSerializer(source="member", read_only=True)

    class Meta:
        model = BookLoan
        fields = "__all__"


class MemberLoanSerializer(BookLoanSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["is_overdue"] = instance.due_date < timezone.now()
        return data

    class Meta:
        model = BookLoan
        fields = ["book", "loan_date", "due_date", "is_overdue"]
