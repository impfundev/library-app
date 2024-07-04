from django.urls import path
from .views import index, update, delete

urlpatterns = [
    path("", index, name="book_list"),
    path("<int:id>/update/", update, name="book_update"),
    path("<int:id>/delete/", delete, name="book_delete"),
]
