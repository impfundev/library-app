from django.urls import path
from books.views import index, update, delete

urlpatterns = [
    path("", index, name="book_lists"),
    path("<id>/update/", update, name="update_book"),
    path("<id>/delete/", delete, name="delete_book"),
]
