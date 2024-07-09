from django.db import models
from members.utils import generate_unique_number

random_number = generate_unique_number(15)


class Members(models.Model):
    account_number = models.CharField(
        default=random_number, editable=False, max_length=15
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "members"
