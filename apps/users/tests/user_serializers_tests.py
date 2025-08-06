from typing import Any

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware

from rest_framework.test import APIRequestFactory

from apps.users.serializers import (
    CustomRegisterSerializer,
)

User = get_user_model()


class CustomRegisterSerializerTests(TestCase):
    """
    Tests for the CustomRegisterSerializer.
    Ensures correct validation and user creation.
    """

    def setUp(self) -> None:
        super().setUp()
        self.factory = APIRequestFactory()
        self.user_data = {
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
            "agreed_to_terms": True,
        }

    def create_user(self, **params: Any):
        data = self.user_data
        data.pop("password1")
        data.pop("password2")
        data["password"] = "Test-Secure-PWD-11"
        data.update(params)
        return User.objects.create_user(**data)

    def test_valid_registration_data(self):
        """
        Test serializer with valid registration data.
        """
        serializer = CustomRegisterSerializer(data=self.user_data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid(), serializer.errors)
        request = self.factory.post("/")
        middleware = SessionMiddleware(get_response=lambda r: r)
        middleware.process_request(request)
        request.session.save()
        user = serializer.save(request)  # Pass a dummy request object

        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.full_name, "Test User")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_business_user)
        self.assertFalse(user.is_company_admin)

    def test_missing_email(self):
        """
        Test registration with missing email.
        """
        data = self.user_data
        data.pop("email")
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("This field is required.", serializer.errors["email"])

    def test_missing_first_name(self):
        """
        Test registration with missing first_name.
        """
        data = self.user_data
        data.pop("first_name")
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("This field is required.", serializer.errors["first_name"])

    def test_missing_last_name(self):
        """
        Test registration with missing last_name.
        """
        data = self.user_data
        data.pop("last_name")
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)
        self.assertIn("This field is required.", serializer.errors["last_name"])

    def test_password_mismatch(self):
        """
        Test registration with mismatched passwords.
        """
        data = self.user_data
        data["password2"] = "securepassword1234"
        serializer = CustomRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "The two password fields didn't match.", serializer.errors["detail"]
        )

    def test_duplicate_email(self):
        """
        Test registration with an email that already exists.
        """
        self.create_user()
        serializer = CustomRegisterSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        # The exact error message for duplicate email might vary slightly based on allauth version
        self.assertIn(
            "A user with that email already exists.",
            serializer.errors["email"],
        )

    def test_full_name_generation_on_save(self):
        """
        Test that full_name is correctly set by the serializer's save method.
        """
        serializer = CustomRegisterSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        request = self.factory.post("/")
        middleware = SessionMiddleware(get_response=lambda r: r)
        middleware.process_request(request)
        request.session.save()
        user = serializer.save(request)
        self.assertEqual(user.full_name, "Test User")

        # Test with empty first/last name
        data_no_names = self.user_data
        data_no_names["email"] = "nonameserializer@example.com"
        data_no_names["first_name"] = ""
        data_no_names["last_name"] = ""
        serializer_no_names = CustomRegisterSerializer(data=data_no_names)
        self.assertFalse(serializer_no_names.is_valid())
        self.assertIn("first_name", serializer_no_names.errors)
        self.assertIn("last_name", serializer_no_names.errors)
