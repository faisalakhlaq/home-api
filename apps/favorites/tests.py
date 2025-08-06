from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APIRequestFactory

from apps.favorites.models import UserFavoriteProperty
from apps.properties.models.property import Property, PropertyStatus, PropertyType

UserModel = get_user_model()


class TestUserFavoritePropertiesAPI(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.list_url: str = reverse("apps.favorites:favorite-list")
        cls.detail_url: str = "apps.favorites:favorite-detail"

        cls.property_payload = {
            "price": "50000",
            "price_currency": "Euro",
            "area": 110.0,
            "total_area": 130.0,
            "total_rooms": 4.0,
            "description": "Комфорен стан на адреса Маршал Тито во Кичево",
            "street_name": "Maršal Tito",
            "city": "Kičevo",
            "region": "R12",
            "postal_code": "6250",
            "country_code": "MK",
            "status": PropertyStatus.ACTIVE,
            "property_type": PropertyType.APARTMENT,
        }

        # Create a test user
        cls.user = UserModel.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="Test",
            agreed_to_terms=True,
        )

    def setUp(self) -> None:
        super().setUp()
        # The client may store state (e.g., authentication tokens) that
        # shouldn’t leak between tests. Therefore, keep in setUp.
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def create_property(self, **params):
        payload = dict(self.property_payload)
        payload.update(params)
        return Property.objects.create(**payload)

    def test_create_favorite_property(self) -> None:
        self.client.force_authenticate(user=self.user)
        property_instance = self.create_property()
        payload = {"property_id": property_instance.id}
        res = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(
            UserFavoriteProperty.objects.filter(
                user=self.user, property=property_instance
            ).exists()
        )
        self.assertEqual(UserFavoriteProperty.objects.count(), 1)
        self.assertEqual(res.json()["property"]["id"], property_instance.id)
        self.assertEqual(res.json()["user"], self.user.id)

    def test_create_duplicate_favorite(self) -> None:
        self.client.force_authenticate(user=self.user)
        property_instance = self.create_property()

        # First creation (should succeed)
        payload = {"property_id": property_instance.id}
        res_first = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(res_first.status_code, 201)

        # Second creation (should fail with 409 Conflict)
        res_second = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(res_second.status_code, 409)
        self.assertIn("already in your favorites", res_second.json()["detail"])
        # Ensure only one favorite entry exists
        self.assertEqual(UserFavoriteProperty.objects.count(), 1)

    def test_create_favorite_unauthenticated(self) -> None:
        property_instance = self.create_property()
        payload = {"property_id": property_instance.id}
        res = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(res.status_code, 401)
        self.assertIn(
            "Authentication credentials were not provided.", res.json()["detail"]
        )

    def test_create_favorite_with_invalid_property_id(self) -> None:
        self.client.force_authenticate(user=self.user)
        # Use an ID that does not exist
        payload = {"property_id": 99999}
        res = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(res.status_code, 400)
        # Expecting an error message about object not found
        self.assertIn("Invalid pk", res.json()["property_id"][0])

    def test_list_favorites_authenticated(self) -> None:
        """
        Test that an authenticated user can list their favorite properties.
        """
        self.client.force_authenticate(user=self.user)
        property1 = self.create_property()
        property2 = self.create_property()

        # Create favorite entries for the user
        UserFavoriteProperty.objects.create(user=self.user, property=property1)
        UserFavoriteProperty.objects.create(user=self.user, property=property2)

        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 2)
        # Check if the properties are in the response by their IDs
        res_property_ids = {item["property"]["id"] for item in res.json()}
        self.assertIn(property1.id, res_property_ids)
        self.assertIn(property2.id, res_property_ids)

    def test_list_favorites_unauthenticated(self) -> None:
        """
        Test that an unauthenticated user cannot list favorites.
        """
        property1 = self.create_property()
        UserFavoriteProperty.objects.create(user=self.user, property=property1)

        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 401)
        self.assertIn(
            "Authentication credentials were not provided.", res.json()["detail"]
        )

    def test_retrieve_favorite_authenticated_owner(self) -> None:
        """
        Test that an authenticated user can retrieve their own favorite property.
        """
        property_instance = self.create_property()
        favorite_instance = UserFavoriteProperty.objects.create(
            user=self.user, property=property_instance
        )
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": favorite_instance.id}
        )

        self.client.force_authenticate(user=self.user)
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], favorite_instance.id)
        self.assertEqual(res.json()["property"]["id"], property_instance.id)

    def test_retrieve_favorite_authenticated_other_user(self) -> None:
        """
        Test that an authenticated user cannot retrieve another user's favorite.
        """
        other_user = UserModel.objects.create_user(
            username="testuserAnother",
            email="test123@example.com",
            password="testpass123",
            first_name="Test",
            last_name="Test",
            agreed_to_terms=True,
        )
        property_instance = self.create_property()
        other_favorite_instance = UserFavoriteProperty.objects.create(
            user=other_user, property=property_instance
        )
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": other_favorite_instance.id}
        )

        self.client.force_authenticate(user=self.user)  # Authenticate as self.user
        res = self.client.get(detail_url)
        # Expect 404 because get_queryset filters out favorites not owned by self.user
        self.assertEqual(res.status_code, 404)

    def test_retrieve_favorite_unauthenticated(self) -> None:
        """
        Test that an unauthenticated user cannot retrieve a favorite.
        """
        property_instance = self.create_property()
        favorite_instance = UserFavoriteProperty.objects.create(
            user=self.user, property=property_instance
        )
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": favorite_instance.id}
        )

        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, 401)

    def test_destroy_favorite_authenticated_owner(self) -> None:
        """
        Test that an authenticated user can delete their own favorite property.
        """
        property_instance = self.create_property()
        favorite_instance = UserFavoriteProperty.objects.create(
            user=self.user, property=property_instance
        )
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": favorite_instance.id}
        )

        self.client.force_authenticate(user=self.user)
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, 204)  # No content on successful delete
        self.assertFalse(
            UserFavoriteProperty.objects.filter(id=favorite_instance.id).exists()
        )
        self.assertEqual(UserFavoriteProperty.objects.count(), 0)

    def test_destroy_favorite_authenticated_other_user(self) -> None:
        """
        Test that an authenticated user cannot delete another user's favorite.
        """
        other_user = UserModel.objects.create_user(
            username="testuserAnother",
            email="another@example.com",
            password="anotherpass123",
            first_name="Test",
            last_name="Test",
            agreed_to_terms=True,
        )
        property_instance = self.create_property()
        other_favorite_instance = UserFavoriteProperty.objects.create(
            user=other_user, property=property_instance
        )
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": other_favorite_instance.id}
        )

        self.client.force_authenticate(user=self.user)  # Authenticate as self.user
        res = self.client.delete(detail_url)
        # Expect 404 because get_queryset filters out favorites not owned by self.user
        self.assertEqual(res.status_code, 404)
        # Ensure the other user's favorite still exists
        self.assertTrue(
            UserFavoriteProperty.objects.filter(id=other_favorite_instance.id).exists()
        )

    def test_destroy_favorite_unauthenticated(self) -> None:
        """
        Test that an unauthenticated user cannot delete a favorite.
        """
        property_instance = self.create_property()
        favorite_instance = UserFavoriteProperty.objects.create(
            user=self.user, property=property_instance
        )
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": favorite_instance.id}
        )

        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(
            UserFavoriteProperty.objects.filter(id=favorite_instance.id).exists()
        )

    def test_destroy_favorite_non_existent(self) -> None:
        """
        Test that deleting a non-existent favorite returns 404.
        """
        self.client.force_authenticate(user=self.user)
        non_existent_id = 99999
        detail_url = reverse(
            "apps.favorites:favorite-detail", kwargs={"pk": non_existent_id}
        )

        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, 404)

    def tearDown(self) -> None:
        return super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
