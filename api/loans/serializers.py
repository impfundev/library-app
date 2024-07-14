from rest_framework import serializers

from loans.models import BookLoan


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = "__all__"
