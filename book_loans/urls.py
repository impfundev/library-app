from django.urls import path
from book_loans.views import index, update, delete

urlpatterns = [
    path("", index, name="book_loan_lists"),
    path("<id>/update/", update, name="update_book"),
    path("<id>/delete/", delete, name="delete_book_loan"),
]
