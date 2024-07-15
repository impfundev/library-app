from django.urls import path
from .views import (
    BookLoanListView,
    BookLoanCreateView,
    BookLoanUpdateView,
    BookLoanDeleteView,
)

urlpatterns = [
    path("", BookLoanListView.as_view(), name="book_loan_lists"),
    path("add/", BookLoanCreateView.as_view(), name="add_book_loan"),
    path("<int:pk>/", BookLoanUpdateView.as_view(), name="update_book_loan"),
    path("<int:pk>/delete/", BookLoanDeleteView.as_view(), name="delete_book_loan"),
]
