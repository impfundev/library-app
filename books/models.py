from datetime import datetime
from django.db import models
from categories.models import Category
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    stock = models.BigIntegerField(blank=True, null=True)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, blank=True, null=True
    )
    cover_image = models.ImageField(upload_to="uploads", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
        help_text="E.g: 2024",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "book"
