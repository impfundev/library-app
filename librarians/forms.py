from django import forms
from librarians.models import Librarians


class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarians
        fields = ["name", "email", "password"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Name",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "form-control",
                }
            ),
            "password": forms.TextInput(
                attrs={
                    "placeholder": "Password",
                    "class": "form-control",
                }
            ),
        }
