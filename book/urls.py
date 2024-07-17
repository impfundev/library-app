from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("add/", BookCreateView.as_view(), name="book_add"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/add/", CategoryCreateView.as_view(), name="category_update"),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
