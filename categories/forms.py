from django import forms
from categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Title",
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
