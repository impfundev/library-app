from django.urls import path, include
from rest_framework import routers

from .auth.views import (
    LibrarianViewSet,
    LibrarianLoginView,
    LibrarianLogoutView,
    MemberViewSet,
    MemberLoginView,
    MemberLogoutView,
)
from .book.views import BookViewSet, CategoryViewSet
from .loans.views import (
    BookLoanViewSet,
    OverduedBookLoanViewSet,
    UpComingBookLoanViewSet,
)


router = routers.DefaultRouter()
router.register(r"librarians", LibrarianViewSet, basename="librarians")
router.register(r"members", MemberViewSet, basename="members")
router.register(r"books", BookViewSet, basename="books")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"book-loans", BookLoanViewSet, basename="book_loans")
router.register(
    r"overdued-loans", OverduedBookLoanViewSet, basename="book_loans_overdued"
)
router.register(
    r"upcoming-loans", UpComingBookLoanViewSet, basename="book_loans_upcoming"
)

urlpatterns = [
    path("", include(router.urls)),
    # auth
    path("librarians/auth/login", LibrarianLoginView.as_view(), name="librarian_login"),
    path(
        "librarians/auth/logout", LibrarianLogoutView.as_view(), name="librarian_logout"
    ),
    path("members/auth/login", MemberLoginView.as_view(), name="member_login"),
    path("members/auth/logout", MemberLogoutView.as_view(), name="member_logout"),
]
