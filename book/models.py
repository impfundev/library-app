from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    publish_date = models.DateTimeField()
    rating = models.IntegerField(
        default=0, validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    isbn = models.CharField(max_length=15, default="xxxxxxxxx-x")
    description = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(upload_to="uploads", blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
