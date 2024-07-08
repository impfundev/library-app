from django.urls import path, include
from rest_framework import routers
from api.views import (
    UserViewSet,
    BookViewSet,
    MemberViewSet,
    LibrarianViewSet,
    BookLoanViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"books", BookViewSet, basename="books")
router.register(r"members", MemberViewSet, basename="members")
router.register(r"librarians", LibrarianViewSet, basename="librarians")
router.register(r"book_loans", BookLoanViewSet, basename="book_loans")

urlpatterns = [
    path("", include(router.urls)),
]
