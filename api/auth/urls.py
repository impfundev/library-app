from django.urls import path, include
from rest_framework import routers

from .views import (
    LibrarianViewSet,
    LibrarianLoginView,
    LibrarianLogoutView,
    MemberViewSet,
    MemberLoginView,
    MemberLogoutView,
)

router = routers.DefaultRouter()
router.register(r"librarians", LibrarianViewSet, basename="librarians")
router.register(r"members", MemberViewSet, basename="members")

urlpatterns = [
    path("", include(router.urls)),
    path("librarians/auth/login", LibrarianLoginView.as_view(), name="librarian_login"),
    path(
        "librarians/auth/logout", LibrarianLogoutView.as_view(), name="librarian_logout"
    ),
    path("members/auth/login", MemberLoginView.as_view(), name="member_login"),
    path("members/auth/logout", MemberLogoutView.as_view(), name="member_logout"),
]
