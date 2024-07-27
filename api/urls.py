from django.urls import path, include
from rest_framework import routers

from .auth.views import (
    LibrarianViewSet,
    LibrarianLoginView,
    LibrarianRegisterView,
    LibrarianLoginHistoryViewSet,
    MemberViewSet,
    MemberLoginView,
    MemberRegisterView,
    MemberChangePasswordView,
    LogoutView,
    TokenResetPasswordView,
    ResetPasswordConfirmView,
    UserDetailView,
)
from .book.views import BookViewSet, CategoryViewSet
from .loans.views import (
    BookLoanViewSet,
    OverduedBookLoanViewSet,
    UpComingBookLoanViewSet,
    MemberLoanViewSet,
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
router.register(
    r"login-history", LibrarianLoginHistoryViewSet, basename="librarian_login_history"
)

router_member_loan = routers.DefaultRouter()
router_member_loan.register(r"loans", MemberLoanViewSet, basename="member_loans")

urlpatterns = [
    path("", include(router.urls)),
    # auth
    path(
        "user",
        UserDetailView.as_view(),
        name="user_detail",
    ),
    path(
        "reset-password/request-token",
        TokenResetPasswordView.as_view(),
        name="reset_password_request_token",
    ),
    path(
        "reset-password/confirm",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path("librarians/auth/login", LibrarianLoginView.as_view(), name="librarian_login"),
    path(
        "librarians/auth/register",
        LibrarianRegisterView.as_view(),
        name="librarian_register",
    ),
    path("auth/logout", LogoutView.as_view(), name="librarian_logout"),
    path("members/auth/login", MemberLoginView.as_view(), name="member_login"),
    path(
        "members/auth/register",
        MemberRegisterView.as_view(),
        name="librarian_register",
    ),
    # change password
    path(
        "members/<int:member_id>/change-password",
        MemberChangePasswordView.as_view(),
        name="member_change_password",
    ),
    path(
        "members/<int:member_id>/",
        include(router_member_loan.urls),
        name="member_loans",
    ),
]
