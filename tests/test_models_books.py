from django.test import TestCase
from books.models import Book


class BookModelTestCase(TestCase):
    def setUp(self):
        self.title = "Test Book"
        self.description = "It's just Book created for testing!"

        Book.objects.create(title=self.title, description=self.description)

    def test_get_books(self):
        """Should get all books"""
        books = Book.objects.all()
        self.assertIsNotNone(books)

    def test_get_book_by_field(self):
        """Should get book by field"""
        book = Book.objects.get(title=self.title)
        self.assertEqual(book.title, self.title)

    def test_create_new_book(self):
        """Should create new book"""
        title = "New book"
        description = "This is new book, created just for testing!"
        Book.objects.create(title=title, description=description)

        new_book = Book.objects.get(title=title)
        self.assertEqual(new_book.title, title)
        self.assertEqual(new_book.description, description)

    def test_update_book(self):
        """Should update book fields"""
        new_title = "This is updated title!"
        Book.objects.filter(title=self.title).update(title=new_title)

        updated_book = Book.objects.get(title=new_title)
        self.assertEqual(updated_book.title, new_title)

    def test_delete_book(self):
        book = Book.objects.get(title=self.title)
        book.delete()

        self.assertRaises(Book.DoesNotExist, Book.objects.get, title=book.title)
