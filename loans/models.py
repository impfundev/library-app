from django.db import models

from book.models import Book
from users.models import Member
from .validators import validate_loan_date


class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(validators=[validate_loan_date])
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
