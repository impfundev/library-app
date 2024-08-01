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
        now = timezone.now()
        remaining_loan_time = instance.due_date - now

        days = remaining_loan_time.days
        hours, remainder = divmod(remaining_loan_time.seconds, 3600)
        minutes = remainder // 60

        time_string = ""
        if days > 0:
            time_string += f"{days} days"
        if hours > 0:
            time_string += f" {hours} hrs"
        if minutes > 0:
            time_string += f" {minutes} mins"

        data["remaining_loan_time"] = time_string + " days left"
        data["is_overdue"] = instance.due_date < timezone.now()
        return data

    class Meta:
        model = BookLoan
        fields = "__all__"
