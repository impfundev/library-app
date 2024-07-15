from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        widgets = {
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
            "publish_date": forms.TextInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "isbn": forms.TextInput(
                attrs={
                    "placeholder": "ISBN",
                    "class": "form-control",
                }
            ),
            "cover_image": forms.FileInput(
                attrs={
                    "placeholder": "Cover Image",
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
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
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Description",
                    "class": "form-control",
                }
            ),
        }
