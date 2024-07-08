from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    get_user_model,
    UserSerializer,
    Book,
    BookSerializer,
    Members,
    MemberSerializer,
    Librarians,
    LibrarianSerializer,
    BookLoans,
    BookLoanSerializer,
)


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all().order_by("id")
    serializer_class = UserSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by("created_at")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["title", "description"]
    search_fields = filterset_fields


class MemberViewSet(ModelViewSet):
    queryset = Members.objects.all().order_by("created_at")
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name", "email"]
    search_fields = filterset_fields


class LibrarianViewSet(ModelViewSet):
    queryset = Librarians.objects.all().order_by("created_at")
    serializer_class = LibrarianSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name", "email"]
    search_fields = filterset_fields


class BookLoanViewSet(ModelViewSet):
    queryset = BookLoans.objects.all().order_by("created_at")
    serializer_class = BookLoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "book__title",
        "member__name",
        "librarians__name",
        "loan_date",
        "due_date",
        "return_date",
    ]
    search_fields = filterset_fields
