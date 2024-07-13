from django.urls import path, include
from rest_framework import routers

from .views import LibrarianViewSet, MemberSerializer

router = routers.DefaultRouter()
router.register(r"librarians", LibrarianViewSet, basename="librarians")
router.register(r"members", MemberSerializer, basename="members")

urlpatterns = [
    path("", include(router.urls)),
]
