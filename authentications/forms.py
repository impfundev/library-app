from django import forms
from librarians.models import Librarians


class LoginForm(forms.ModelForm):
    class Meta:
        model = Librarians
        fields = ["email", "password"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "class": "form-control",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Password",
                    "class": "form-control",
                }
            ),
        }


class SignUpForm(forms.ModelForm):
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
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Password",
                    "class": "form-control",
                }
            ),
        }


class ForgotPassword(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        )
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Old Password",
                "class": "form-control",
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control",
            }
        )
    )
