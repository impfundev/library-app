from django.urls import path
from librarians.views import index, update, delete

urlpatterns = [
    path("", index, name="librarian_lists"),
    path("<id>/update/", update, name="update_librarian"),
    path("<id>/delete/", delete, name="delete_librarian"),
]
