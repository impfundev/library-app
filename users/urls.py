from django.urls import path

from users.views import (
    LibrarianListView,
    LibrarianCreateView,
    LibrarianDeleteView,
    LibrarianUpdateView,
    LibrarianLoginHistoryView,
    MemberListView,
    MemberCreateView,
    MemberDeleteView,
    MemberUpdateView,
)

urlpatterns = [
    # librarians
    path("librarians/", LibrarianListView.as_view(), name="librarian_lists"),
    path("librarians/add/", LibrarianCreateView.as_view(), name="create_librarian"),
    path(
        "librarians/<int:pk>/", LibrarianUpdateView.as_view(), name="update_librarian"
    ),
    path(
        "librarians/<int:pk>/delete/",
        LibrarianDeleteView.as_view(),
        name="delete_librarian",
    ),
    path(
        "librarians/login-history/",
        LibrarianLoginHistoryView.as_view(),
        name="librarian_login_history",
    ),
    # members
    path("members/", MemberListView.as_view(), name="member_lists"),
    path("members/add/", MemberCreateView.as_view(), name="create_member"),
    path("members/<int:pk>/", MemberUpdateView.as_view(), name="update_member"),
    path("members/<int:pk>/delete/", MemberDeleteView.as_view(), name="delete_member"),
]
