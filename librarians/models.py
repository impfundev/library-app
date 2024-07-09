from django.db import models
from django.contrib.auth.models import User


class Librarians(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "librarians"


class LoginHistory(models.Model):
    librarian = models.ForeignKey(to=Librarians, on_delete=models.CASCADE)
    login_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "librarians_login_histories"
