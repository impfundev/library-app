from django.urls import path, include

from users.views import (
    LibrarianListView,
    LibrarianCreateView,
    LibrarianDeleteView,
    LibrarianUpdateView,
    MemberListView,
    MemberCreateView,
    MemberDeleteView,
    MemberUpdateView,
)
from dashboard.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
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
    # members
    path("members/", MemberListView.as_view(), name="member_lists"),
    path("members/add/", MemberCreateView.as_view(), name="create_member"),
    path("members/<int:pk>/", MemberUpdateView.as_view(), name="update_member"),
    path("members/<int:pk>/delete/", MemberDeleteView.as_view(), name="delete_member"),
    # path("categories/", include("categories.urls")),
    # path("book-loans/", include("book_loans.urls")),
    # path("upcoming-loans/", UpcomingLoanView.as_view(), name="upcoming_loans"),
    # path("overdued-loans/", OverduedLoanView.as_view(), name="overdued_loans"),
]
