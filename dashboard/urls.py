from django.urls import path
from dashboard.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # path("categories/", include("categories.urls")),
    # path("book-loans/", include("book_loans.urls")),
    # path("upcoming-loans/", UpcomingLoanView.as_view(), name="upcoming_loans"),
    # path("overdued-loans/", OverduedLoanView.as_view(), name="overdued_loans"),
]
