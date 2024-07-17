from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import BookLoan, Book, Member


class BookLoanModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publish_date=timezone.now(),
            rating=5,
        )
        self.user = User.objects.create_user(
            username="Test User", password="secret", is_staff=False
        )
        self.member = Member.objects.create(user=self.user)
        self.loan_date = timezone.now()
        self.due_date = self.loan_date + timezone.timedelta(days=14)

    def test_book_loan_creation(self):

        book_loan = BookLoan.objects.create(
            book=self.book,
            member=self.member,
            loan_date=self.loan_date,
            due_date=self.due_date,
        )

        self.assertEqual(book_loan.book, self.book)
        self.assertEqual(book_loan.member, self.member)
        self.assertEqual(book_loan.due_date, self.due_date)

    def test_cascading_delete(self):
        book_loan = BookLoan.objects.create(
            book=self.book,
            member=self.member,
            loan_date=self.loan_date,
            due_date=self.due_date,
        )
        book_loan_id = book_loan.id

        self.book.delete()

        with self.assertRaises(BookLoan.DoesNotExist):
            BookLoan.objects.get(id=book_loan_id)
