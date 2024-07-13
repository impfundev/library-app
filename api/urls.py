from django.urls import path, include
from rest_framework import routers

from .views import LibrarianViewSet, MemberViewSet

router = routers.DefaultRouter()
router.register(r"librarians", LibrarianViewSet, basename="librarians")
router.register(r"members", MemberViewSet, basename="members")

urlpatterns = [
    path("", include(router.urls)),
]
