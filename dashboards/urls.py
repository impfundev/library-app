from django.urls import path, include
from dashboards.views import index
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path(
        "",
        cache_page(settings.CACHE_TTL, key_prefix="dashboard")(index),
        name="dashboard",
    ),
    path("books/", include("books.urls")),
    path("members/", include("members.urls")),
    path("book-loans/", include("book_loans.urls")),
    path("librarians/", include("librarians.urls")),
]
