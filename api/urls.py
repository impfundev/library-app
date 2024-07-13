from django.urls import path, include

from .auth import urls as auth_urls

urlpatterns = [
    path("", include(auth_urls)),
]
