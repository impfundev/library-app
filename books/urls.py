from django.urls import path
from .views import index, update, delete
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path(
        "",
        cache_page(settings.CACHE_TTL, key_prefix="books")(index),
        name="book_list",
    ),
    path("<int:id>/update/", update, name="book_update"),
    path("<int:id>/delete/", delete, name="book_delete"),
]
