from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Category, Book


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")

    def test_category_update(self):
        self.category.name = "Test Category Update"
        self.category.save()
        self.assertEqual(self.category.name, "Test Category Update")

    def test_delete_category(self):
        category = Category.objects.create(name="Test Delete Category")
        category.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category.id)


class BookModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publish_date=timezone.now(),
            rating=3,
            isbn="1234567890123",
            category=self.category,
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.rating, 3)
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(self.book.category, self.category)

    def test_book_update(self):
        self.book.title = "Test Book Update"
        self.book.save()
        self.assertEqual(self.book.title, "Test Book Update")

    def test_delete_book(self):
        book = Book.objects.create(
            title="Test Book 2",
            author="Test Author 2",
            publish_date=timezone.now(),
            rating=3,
            isbn="2234567890123",
        )
        book.delete()

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book.id)
