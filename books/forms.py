from django import forms


class BookForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
                "class": "form-control",
            }
        ),
    )
    description = forms.CharField(
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Description",
                "class": "form-control",
            }
        ),
    )
