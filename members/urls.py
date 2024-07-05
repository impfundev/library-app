from django.urls import path
from members.views import index, update, delete
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path(
        "",
        cache_page(settings.CACHE_TTL, key_prefix="members")(index),
        name="member_lists",
    ),
    path("<id>/update/", update, name="update_member"),
    path("<id>/delete/", delete, name="delete_member"),
]
