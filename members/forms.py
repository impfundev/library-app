from django import forms


class MemberForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control",
            }
        ),
    )
    email = forms.CharField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )
