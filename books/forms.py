from django import forms
from books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["cover_image", "title", "stock", "category", "description"]

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
            "stock": forms.TextInput(
                attrs={
                    "type": "number",
                    "placeholder": "Stock",
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
        }
