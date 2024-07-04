from django import forms
from members.models import Members


class MemberForm(forms.ModelForm):

    class Meta:
        model = Members
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
