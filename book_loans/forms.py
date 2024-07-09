from django import forms
from book_loans.models import BookLoans


class BookLoanForm(forms.ModelForm):
    class Meta:
        model = BookLoans
        fields = [
            "book",
            "member",
            "librarian",
            "loan_date",
            "due_date",
            "return_date",
            "notes",
        ]
        widgets = {
            "book": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "member": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "librarian": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "loan_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "due_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "return_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "placeholder": "Note",
                    "class": "form-control",
                }
            ),
        }
