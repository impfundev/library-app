from django.urls import path
from members.views import (
    MemberListView,
    MemberUpdateView,
    MemberCreateView,
    MemberDeleteView,
)

urlpatterns = [
    path("", MemberListView.as_view(), name="member_lists"),
    path("add/", MemberCreateView.as_view(), name="add_member"),
    path("<int:pk>/", MemberUpdateView.as_view(), name="update_member"),
    path("<int:pk>/delete/", MemberDeleteView.as_view(), name="delete_member"),
]
