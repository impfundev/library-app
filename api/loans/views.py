from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import BookLoan, BookLoanSerializer
from ..auth.permissions import IsNotStaffUser, IsStaffUser


class BookLoanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffUser]
    queryset = BookLoan.objects.all().order_by("loan_date")
    serializer_class = BookLoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["loan_date", "due_date", "return_date"]
    search_fields = [
        "member__user__username",
        "member__user__email",
        "member__user__first_name",
        "member__user__last_name",
        "book__title",
    ]

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OverduedBookLoanViewSet(BookLoanViewSet):
    now = timezone.now()
    queryset = (
        BookLoan.objects.all()
        .filter(due_date__lte=now, return_date=None)
        .order_by("loan_date")
    )


class UpComingBookLoanViewSet(BookLoanViewSet):
    now = timezone.now()
    due_date_treshold = now + timezone.timedelta(days=3)
    queryset = (
        BookLoan.objects.all()
        .filter(due_date__lte=due_date_treshold, return_date=None)
        .filter(due_date__gte=now)
        .order_by("loan_date")
    )


class MemberLoanViewSet(BookLoanViewSet):
    permission_classes = [IsNotStaffUser]
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer

    def get_queryset(self):
        member_id = self.kwargs.get("member_id")

        now = timezone.now()
        due_date_treshold = now + timezone.timedelta(days=3)
        near_outstanding = self.request.query_params.get("near_outstanding")
        overdue = self.request.query_params.get("overdue")

        if near_outstanding:
            return (
                BookLoan.objects.filter(member=member_id)
                .filter(due_date__lte=due_date_treshold, return_date=None)
                .filter(due_date__gte=now)
                .order_by("loan_date")
            )

        if overdue:
            return (
                BookLoan.objects.filter(member=member_id)
                .filter(due_date__lte=now, return_date=None)
                .order_by("loan_date")
            )

        return BookLoan.objects.filter(member=member_id).order_by("loan_date")
