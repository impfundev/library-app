from django.contrib.auth.models import User
from django.db import models

ROLE_CHOICES = (
    ("1", "librarian"),
    ("2", "member"),
)


class Role(models.Model):
    name = models.CharField(choices=ROLE_CHOICES, max_length=50)

    def __str__(self):
        return self.name
