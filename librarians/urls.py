from django.urls import path
from librarians.views import (
    LibrarianListView,
    LibrarianCreateView,
    LibrarianUpdateView,
    LibrarianDeleteView,
)

urlpatterns = [
    path("", LibrarianListView.as_view(), name="librarian_lists"),
    path("add/", LibrarianCreateView.as_view(), name="create_librarian"),
    path("<int:pk>/", LibrarianUpdateView.as_view(), name="update_librarian"),
    path("<int:pk>/delete/", LibrarianDeleteView.as_view(), name="delete_librarian"),
]
