from django.test import TestCase
from .models import Librarian, Member, User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create user data for testing"""
        staff_user = User.objects.create_user(
            username="staff", password="secret", is_staff=True
        )
        regular_user = User.objects.create_user(
            username="member", password="secret", is_staff=False
        )
        cls.librarian = Librarian.objects.create(user=staff_user)
        cls.member = Member.objects.create(user=regular_user)

    def test_librarian_creation(self):
        """Test that a Librarian object can be created with a valid staff user"""
        self.assertEqual(self.librarian.user.username, "staff")

    def test_member_creation(self):
        """Test that a Member object can be created with a valid non-staff user"""
        self.assertEqual(self.member.user.username, "member")

    def test_librarian_update(self):
        """Test updating a Librarian object"""
        new_user = User.objects.create_user(
            username="new_staff", password="secret", is_staff=True
        )
        self.librarian.user = new_user
        self.librarian.save()
        self.assertEqual(self.librarian.user.username, "new_staff")

    def test_member_update(self):
        """Test updating a Member object"""
        new_user = User.objects.create_user(
            username="new_member", password="secret", is_staff=False
        )
        self.member.user = new_user
        self.member.save()
        self.assertEqual(self.member.user.username, "new_member")

    def test_librarian_delete(self):
        """Test deleting a Librarian object"""
        librarian_pk = self.librarian.pk
        self.librarian.delete()
        self.assertFalse(Librarian.objects.filter(pk=librarian_pk).exists())

    def test_member_delete(self):
        """Test deleting a Member object"""
        member_pk = self.member.pk
        self.member.delete()
        self.assertFalse(Member.objects.filter(pk=member_pk).exists())
