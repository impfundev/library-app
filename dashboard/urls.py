from django.urls import path, include
from dashboard.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("books/", include("book.urls")),
    # path("categories/", include("categories.urls")),
    # path("members/", include("members.urls")),
    # path("book-loans/", include("book_loans.urls")),
    # path("librarians/", include("librarians.urls")),
    # path("upcoming-loans/", UpcomingLoanView.as_view(), name="upcoming_loans"),
    # path("overdued-loans/", OverduedLoanView.as_view(), name="overdued_loans"),
]
