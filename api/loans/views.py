from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import BookLoan, BookLoanSerializer


class BookLoanViewSet(viewsets.ModelViewSet):
    queryset = BookLoan.objects.all().order_by("loan_date")
    serializer_class = BookLoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["loan_date", "due_date", "return_date", "member__id"]
    search_fields = ["book__title", "member__name"]

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
