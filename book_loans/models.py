from django.db import models
from books.models import Book
from members.models import Members
from librarians.models import Librarians


class BookLoans(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(to=Members, on_delete=models.SET_NULL, null=True)
    librarians = models.ForeignKey(to=Librarians, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    loan_date = models.DateTimeField()
    due_date = models.DateTimeField()
    return_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "book_loans"
