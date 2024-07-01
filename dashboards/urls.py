from django.urls import path, include
from dashboards.views import index

urlpatterns = [
    path("", index, name="dashboard"),
    path("books/", include("books.urls")),
    path("members/", include("members.urls")),
    path("librarians/", include("librarians.urls")),
]
