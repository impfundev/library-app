from django.urls import path, include
from rest_framework import routers

from .auth.views import (
    registerUserView,
    loginUserView,
    logoutUserView,
    getUserDetail,
    memberLoanView,
    updateUserProfileView,
    checkAuthSessionView,
    changePasswordView,
    resetPasswordView,
    resetPasswordConfirmView,
)

from .book.views import bookView, CategoryViewSet
from .loans.views import (
    BookLoanViewSet,
    OverduedBookLoanViewSet,
    UpComingBookLoanViewSet,
    MemberLoanViewSet,
)


router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"book-loans", BookLoanViewSet, basename="book_loans")
router.register(
    r"overdued-loans", OverduedBookLoanViewSet, basename="book_loans_overdued"
)
router.register(
    r"upcoming-loans", UpComingBookLoanViewSet, basename="book_loans_upcoming"
)

router_member_loan = routers.DefaultRouter()
router_member_loan.register(r"loans", MemberLoanViewSet, basename="member_loans")

urlpatterns = [
    path("", include(router.urls)),
    # auth
    path("user", getUserDetail, name="user_detail"),
    path("user/loans", memberLoanView, name="user_loans"),
    path("user/update", updateUserProfileView, name="update_user_profile"),
    path("auth/login", loginUserView, name="login"),
    path("auth/logout", logoutUserView, name="logout"),
    path("auth/register", registerUserView, name="register"),
    path("auth/change-password", changePasswordView, name="change_password"),
    path("auth/reset-password", resetPasswordView, name="reset_password"),
    path(
        "auth/reset-password-confirm",
        resetPasswordConfirmView,
        name="reset_password_confirm",
    ),
    path("auth/check-auth-session", checkAuthSessionView, name="check_auth_session"),
    # books
    path("books", bookView, name="books"),
]
