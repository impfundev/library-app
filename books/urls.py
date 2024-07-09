from django.urls import path
from books.views import BookListView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("add/", BookCreateView.as_view(), name="book_update"),
    path("<int:pk>/", BookUpdateView.as_view(), name="book_update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
]
