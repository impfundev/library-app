from django.db import models
from django.contrib.auth.models import User


class Librarian(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={"is_staff": True}
    )
    picture = models.ImageField(upload_to="uploads", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={"is_staff": False}
    )
    picture = models.ImageField(upload_to="uploads", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class LibrarianLoginHistory(models.Model):
    librarian = models.OneToOneField(
        Librarian, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    date = models.DateTimeField(auto_now_add=True)
