from django.urls import path
from book_loans.views import index, update, delete
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path(
        "",
        cache_page(settings.CACHE_TTL, key_prefix="book_loans")(index),
        name="book_loan_lists",
    ),
    path("<id>/update/", update, name="update_book"),
    path("<id>/delete/", delete, name="delete_book_loan"),
]
