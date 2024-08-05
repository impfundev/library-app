from django.urls import path

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

from .book.views import bookView, categoryView
from .loans.views import bookLoanView

urlpatterns = [
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
    # categories
    path("categories", categoryView, name="categories"),
    # book loans
    path("book-loans", bookLoanView, name="book_loans"),
]
