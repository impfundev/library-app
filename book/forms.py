from django import forms
from .models import Book

"""
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
"""


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        widgets = {
            "cover_image": forms.FileInput(
                attrs={
                    "placeholder": "Cover Image",
                    "class": "form-control",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Title",
                    "class": "form-control",
                }
            ),
            "author": forms.TextInput(
                attrs={
                    "placeholder": "Author",
                    "class": "form-control",
                }
            ),
            "isbn": forms.TextInput(
                attrs={
                    "placeholder": "ISBN",
                    "class": "form-control",
                }
            ),
            "rating": forms.TextInput(
                attrs={
                    "type": "number",
                    "placeholder": "Rating",
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Description",
                    "class": "form-control",
                }
            ),
            "publish_date": forms.TextInput(
                attrs={
                    "type": "number",
                    "class": "form-control",
                }
            ),
        }
