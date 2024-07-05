from django.urls import path
from librarians.views import index, update, delete
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path(
        "",
        cache_page(settings.CACHE_TTL, key_prefix="librarians")(index),
        name="librarian_lists",
    ),
    path("<id>/update/", update, name="update_librarian"),
    path("<id>/delete/", delete, name="delete_librarian"),
]
