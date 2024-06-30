from django.urls import path, include
from dashboards.views import home, index

urlpatterns = [
    path("", index, name="dashboard"),
    path("books/", include("books.urls")),
    path("members/", include("members.urls")),
]
