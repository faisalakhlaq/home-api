# apps/users/tests/test_api.py
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):
    """
    Tests for the user registration and details API endpoints.
    """

    def setUp(self):
        # URLs for dj-rest-auth endpoints
        self.register_url = reverse("apps.users:rest_register")
        self.login_url = reverse("apps.users:rest_login")
        self.user_details_url = reverse("apps.users:rest_user_details")

        self.data = {
            "email": "newapiuser@example.com",
            "password1": "api_secure_password",
            "password2": "api_secure_password",
            "first_name": "API",
            "last_name": "User",
            "agreed_to_terms": True,
        }
        # Create a sample user for login/details tests if needed
        self.user_password = "testpassword123"
        self.user = User.objects.create_user(
            email="existing@example.com",
            password=self.user_password,
            first_name="Existing",
            last_name="User",
            agreed_to_terms=True,
        )

    def test_user_registration_success(self):
        """
        Test successful user registration via API.
        """
        response = self.client.post(self.register_url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)  # Check for auth token
        self.assertEqual(User.objects.count(), 2)  # Initial user + new user

        new_user = User.objects.get(email="newapiuser@example.com")
        self.assertEqual(new_user.first_name, "API")
        self.assertEqual(new_user.last_name, "User")
        self.assertEqual(new_user.full_name, "API User")
        self.assertTrue(new_user.check_password("api_secure_password"))

    def test_user_registration_missing_email(self):
        """
        Test registration with missing email field.
        """
        data = self.data
        data.pop("email")
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_user_registration_missing_first_name(self):
        """
        Test registration with missing first_name field.
        """
        data = self.data
        data.pop("first_name")
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)

    def test_user_registration_duplicate_email(self):
        """
        Test registration with an email that already exists.
        """
        data = self.data
        data["email"] = "existing@example.com"  # This email already exists from setUp
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn(
            "A user with that email already exists.",
            response.data["email"],
        )

    def test_user_details_authenticated(self):
        """
        Test retrieving user details for an authenticated user.
        """
        # Log in the user created in setUp
        login_data = {"email": self.user.email, "password": self.user_password}
        login_response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data["access"]

        # Set the authorization header with the obtained token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        details_response = self.client.get(self.user_details_url, format="json")

        self.assertEqual(details_response.status_code, status.HTTP_200_OK)
        self.assertEqual(details_response.data["email"], self.user.email)
        self.assertEqual(details_response.data["first_name"], self.user.first_name)
        self.assertEqual(details_response.data["last_name"], self.user.last_name)
        self.assertEqual(details_response.data["full_name"], self.user.full_name)
        # Check other custom fields if you want them exposed by UserDetailsSerializer
        self.assertIn("is_business_user", details_response.data)
        self.assertIn("is_company_admin", details_response.data)

    def test_user_details_unauthenticated(self):
        """
        Test retrieving user details without authentication.
        """
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
