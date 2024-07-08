from django.urls import path
from members.views import index, update, delete

urlpatterns = [
    path("", index, name="member_lists"),
    path("<id>/update/", update, name="update_member"),
    path("<id>/delete/", delete, name="delete_member"),
]
