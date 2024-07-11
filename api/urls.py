from django.urls import path, include
from rest_framework import routers
from api.views import (
    UserViewSet,
    BookViewSet,
    MemberViewSet,
    LibrarianViewSet,
    BookLoanViewSet,
    LoginAsLibrarian,
    LogoutAsLibrarian,
    ChangePasswordAsLibrarian,
    LoginAsMember,
    LogoutAsMember,
    ChangePasswordAsMember,
    OverduedBookLoanViewSet,
    UpComingBookLoanViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"books", BookViewSet, basename="books")
router.register(r"members", MemberViewSet, basename="members")
router.register(r"librarians", LibrarianViewSet, basename="librarians")
router.register(r"book-loans", BookLoanViewSet, basename="book_loans")
router.register(
    r"overdued-loans", OverduedBookLoanViewSet, basename="book_loans_overdued"
)
router.register(
    r"upcoming-loans", UpComingBookLoanViewSet, basename="book_loans_upcoming"
)

urlpatterns = [
    path("", include(router.urls)),
    path("login/librarian/", LoginAsLibrarian.as_view(), name="login_librarian"),
    path(
        "logout/librarian/<int:pk>/",
        LogoutAsLibrarian.as_view(),
        name="logout_librarian",
    ),
    path(
        "librarians/<int:pk>/change_password/",
        ChangePasswordAsLibrarian.as_view(),
        name="change_pw_librarian",
    ),
    path("login/member/", LoginAsMember.as_view(), name="login_member"),
    path(
        "logout/member/<int:pk>/",
        LogoutAsMember.as_view(),
        name="logout_member",
    ),
    path(
        "members/<int:pk>/change_password/",
        ChangePasswordAsMember.as_view(),
        name="change_pw_member",
    ),
]
