from django import forms


class BookLoanForm(forms.Form):
    loan_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        )
    )
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        )
    )
    return_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        ),
    )
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Note",
                "class": "form-control",
            }
        ),
    )
