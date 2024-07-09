from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    stock = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "book"
