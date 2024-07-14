from django.db import models

from book.models import Book
from users.models import Member


class BookLoan(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
