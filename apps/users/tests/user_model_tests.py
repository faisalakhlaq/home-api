from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    """
    Tests for the custom User model.
    Ensures custom fields, __str__, and save method work correctly.
    """

    def test_create_user(self):
        """
        Test creating a regular user with required fields.
        """
        user = User.objects.create_user(
            email="test@example.com",
            password="strong-password",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("strong-password"))
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.full_name, "John Doe")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_business_user)
        self.assertFalse(user.is_company_admin)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="super-strong-password",
            first_name="Admin",
            last_name="User",
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("super-strong-password"))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.full_name, "Admin User")
        self.assertTrue(admin_user.is_active)

    def test_email_unique(self):
        """
        Test that email addresses must be unique.
        """
        User.objects.create_user(
            email="unique@example.com",
            password="password123",
            first_name="Jane",
            last_name="Doe",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com",
                password="anotherpassword",
                first_name="John",
                last_name="Smith",
            )

    def test_full_name_generation(self):
        """
        Test that the full_name field is correctly generated on save.
        """
        user = User.objects.create_user(
            email="test2@example.com",
            password="password123",
            first_name="Alice",
            last_name="Wonderland",
        )
        self.assertEqual(user.full_name, "Alice Wonderland")

        user.first_name = "Alicia"
        user.save()
        self.assertEqual(user.full_name, "Alicia Wonderland")

        user.last_name = "Smith-Jones"
        user.save()
        self.assertEqual(user.full_name, "Alicia Smith-Jones")

    def test_str_representation(self):
        """
        Test the __str__ method returns the email.
        """
        user = User.objects.create_user(
            email="display@example.com",
            password="password123",
            first_name="Display",
            last_name="Name",
        )
        self.assertEqual(str(user), "display@example.com")

    def test_is_business_user_default(self):
        """
        Test default value of is_business_user.
        """
        user = User.objects.create_user(
            email="business@example.com",
            password="password123",
            first_name="Biz",
            last_name="User",
        )
        self.assertFalse(user.is_business_user)

    def test_is_company_admin_default(self):
        """
        Test default value of is_company_admin.
        """
        user = User.objects.create_user(
            email="company@example.com",
            password="password123",
            first_name="Comp",
            last_name="Admin",
        )
        self.assertFalse(user.is_company_admin)

    def test_custom_fields_set_true(self):
        """
        Test setting custom boolean fields to True.
        """
        user = User.objects.create_user(
            email="custom@example.com",
            password="password123",
            first_name="Custom",
            last_name="User",
            is_business_user=True,
            is_company_admin=True,
        )
        self.assertTrue(user.is_business_user)
        self.assertTrue(user.is_company_admin)
