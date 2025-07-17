from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APIRequestFactory

from apps.core.models import Address, City, Genre, Status
from apps.core.serializers import IdNameListSerializer
from apps.properties.models import Property
from apps.properties.querysets import property_list_queryset
from apps.properties.serializers import (
    PropertyDetailSerializer,
    PropertyListSerializer,
    PropertySerializer,
)
from apps.properties.views import PropertyViewSet

User = get_user_model()


class TestPropertyAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.list_url: str = reverse("apps.properties:properties-list")
        cls.detail_url: str = "apps.properties:properties-detail"
        cls.property_form_url: str = reverse(
            "apps.properties:properties-get-create-property-form-data"
        )

        cls.property_payload = {
            "price": "50000",
            "price_currency": "Euro",
            "area": 110.0,
            "total_area": 130.0,
            "total_rooms": 4.0,
            "description": "Комфорен стан на адреса Маршал Тито во Кичево",
        }
        cls.address_payload = {
            "street": "Maršal Tito",
            "city": "Kičevo",
            "region": "R12",
            "postal_code": "6250",
            "country": "North Mecedonia",
        }
        cls.property_content_type = ContentType.objects.get_for_model(model=Property)

        # Create a test user
        cls.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def setUp(self) -> None:
        super().setUp()
        # The client may store state (e.g., authentication tokens) that
        # shouldn’t leak between tests. Therefore, keep in setUp.
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def create_property(self, **params):
        address = dict(self.address_payload)
        payload = dict(self.property_payload)
        payload["address"] = Address.objects.create(**address)
        payload.update(params)
        return Property.objects.create(**payload)

    def _create_status(self, name: str, **kwargs) -> Status:
        """Helper to create a Status object with default values."""
        payload = {
            "name": name,
            "sorting_order": 1,
            "active": True,
            "description": f"Status for {name}",
            "model": self.property_content_type,
        }
        payload.update(kwargs)  # Allow overriding defaults
        return Status.objects.create(**payload)

    def _create_genre(self, name: str, **kwargs) -> Genre:
        """Helper to create a Genre object with default values."""
        payload = {
            "name": name,
            "sorting_order": 1,
            "active": True,
            "description": f"Genre for {name}",
            "model": self.property_content_type,
        }
        payload.update(kwargs)  # Allow overriding defaults
        return Genre.objects.create(**payload)

    def test_prop_property_list(self) -> None:
        p1 = self.create_property()
        p2 = self.create_property()
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        p1.delete()
        p2.delete()

    def test_prop_retrieve_serializer(self):
        view = PropertyViewSet()
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PropertyDetailSerializer)

    def test_prop_list_serializer_class(self):
        view = PropertyViewSet()
        view.action = "list"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PropertyListSerializer)

    def test_prop_post_serializer_class(self):
        view = PropertyViewSet()
        view.action = "create"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PropertySerializer)

    def test_list_queryset(self):
        view = PropertyViewSet()
        request = self.factory.get("/")
        view.request = request
        view.action = "list"

        # Test unauthenticated case
        queryset = view.get_queryset()
        expected_queryset = (
            property_list_queryset()
        )  # Use the same function as your view
        self.assertQuerySetEqual(queryset, expected_queryset, transform=lambda x: x)

        # Test authenticated case
        request.user = self.user
        queryset = view.get_queryset()
        expected_queryset = property_list_queryset(user_id=self.user.id)
        self.assertQuerySetEqual(queryset, expected_queryset, transform=lambda x: x)

    def test_property_create(self):
        self.client.force_authenticate(user=self.user)

        payload = {**self.property_payload, "address": self.address_payload}
        res = self.client.post(self.list_url, data=payload, format="json")
        response_data = res.json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data["owner"], self.user.id)
        self.assertEqual(response_data["price"], 50000)
        self.assertEqual(response_data["price_currency"], "Euro")
        self.assertEqual(response_data["area"], 110.0)
        self.assertEqual(response_data["total_area"], 130.0)
        self.assertEqual(response_data["measured_area"], None)
        self.assertEqual(response_data["total_rooms"], 4.0)
        self.assertEqual(
            res.data["description"], "Комфорен стан на адреса Маршал Тито во Кичево"
        )
        self.assertIn("address", response_data)
        self.assertEqual(response_data["address"]["street"], "Maršal Tito")

    def test_delete_property_not_allowed(self) -> None:
        prop = self.create_property()
        url = reverse(self.detail_url, kwargs={"pk": prop.pk})
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 405)
        self.assertIn("`Property` deletion is not allowed.", res.data["error"])
        prop.delete()

    def test_create_property_unauthenticated(self):
        response = self.client.post(
            self.list_url, data=self.property_payload, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_create_property_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_payload = {**self.property_payload, "price": ""}
        response = self.client.post(self.list_url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_retrieve_property(self) -> None:
        prop = self.create_property()
        url = reverse(self.detail_url, kwargs={"pk": prop.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["price"], 50000)
        self.assertEqual(res.data["price_currency"], "Euro")
        prop.delete()

    def test_get_create_property_form_data(self) -> None:
        self.client.force_authenticate(user=self.user)
        # create related objects
        self._create_status(name="For Sale", sorting_order=2)
        self._create_status(name="Sold", sorting_order=3)
        self._create_status(name="Rented", sorting_order=1)

        self._create_genre(name="Apartment", sorting_order=1)
        self._create_genre(name="House", sorting_order=2)
        self._create_genre(name="Commercial", sorting_order=3)

        cities_to_create = []
        for i in range(1, 20):
            cities_to_create.append(City(name=f"City {i}", country="DK"))
        City.objects.bulk_create(cities_to_create)

        res = self.client.get(self.property_form_url)
        self.assertEqual(res.status_code, 200)

        # --- Assert Genres ---
        expected_genres_queryset = (
            Genre.objects.only("id", "name").order_by("name").values("id", "name")
        )
        expected_genres_data = IdNameListSerializer(
            expected_genres_queryset, many=True
        ).data
        self.assertEqual(res.data["types"], expected_genres_data)

        # --- Assert Statuses ---
        expected_statuses_queryset = (
            Status.objects.only("id", "name").order_by("name").values("id", "name")
        )
        expected_statuses_data = IdNameListSerializer(
            expected_statuses_queryset, many=True
        ).data
        self.assertEqual(res.data["status"], expected_statuses_data)

        # --- Assert Cities ---
        expected_cities_names = list(
            City.objects.only("name").order_by("name").values_list("name", flat=True)
        )
        self.assertEqual(res.data["cities"], expected_cities_names)

    def test_property_default_ordering(self) -> None:
        """
        Tests if the default ordering (-id) works correctly.
        """
        # Create properties with different creation times/ids
        # Property created later should have a higher ID and thus appear first by default
        p1 = self.create_property(
            price=100, created_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        p2 = self.create_property(
            price=200, created_at=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )
        p3 = self.create_property(
            price=300, created_at=datetime(2023, 1, 3, tzinfo=timezone.utc)
        )

        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)
        data = res.json()

        p_ids = sorted([p1.id, p2.id, p3.id], reverse=True)  # Sort in descending order

        # Check the order of IDs returned by the API
        self.assertEqual(data[0]["id"], p_ids[0])
        self.assertEqual(data[1]["id"], p_ids[1])
        self.assertEqual(data[2]["id"], p_ids[2])

    def test_property_ordering_by_price_asc(self) -> None:
        """
        Tests ordering by 'price' in ascending order.
        """
        p1 = self.create_property(
            price=300, created_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        p2 = self.create_property(
            price=100, created_at=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )  # Lowest price
        p3 = self.create_property(
            price=200, created_at=datetime(2023, 1, 3, tzinfo=timezone.utc)
        )

        res = self.client.get(f"{self.list_url}?ordering=price")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Expected order: p2 (100), p3 (200), p1 (300)
        self.assertEqual(data[0]["id"], p2.id)
        self.assertEqual(data[1]["id"], p3.id)
        self.assertEqual(data[2]["id"], p1.id)

    def test_property_ordering_by_price_desc(self) -> None:
        """
        Tests ordering by 'price' in descending order.
        """
        p1 = self.create_property(
            price=300, created_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )  # Highest price
        p2 = self.create_property(
            price=100, created_at=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )
        p3 = self.create_property(
            price=200, created_at=datetime(2023, 1, 3, tzinfo=timezone.utc)
        )

        res = self.client.get(f"{self.list_url}?ordering=-price")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Expected order: p1 (300), p3 (200), p2 (100)
        self.assertEqual(data[0]["id"], p1.id)
        self.assertEqual(data[1]["id"], p3.id)
        self.assertEqual(data[2]["id"], p2.id)

    def test_property_ordering_multiple_fields(self) -> None:
        """
        Tests ordering by multiple fields (e.g., total_rooms, then -price).
        """
        # Properties with same total_rooms but different prices
        p1 = self.create_property(
            total_rooms=3,
            price=300,
            created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
        )
        p2 = self.create_property(
            total_rooms=2,
            price=100,
            created_at=datetime(2023, 1, 2, tzinfo=timezone.utc),
        )
        p3 = self.create_property(
            total_rooms=3,
            price=200,
            created_at=datetime(2023, 1, 3, tzinfo=timezone.utc),
        )  # Same rooms as p1, lower price

        res = self.client.get(f"{self.list_url}?ordering=total_rooms,-price")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Expected order:
        # p2 (2 rooms) first
        # Then, p1 (3 rooms, 300 price) and p3 (3 rooms, 200 price)
        # For p1 and p3, -price means p1 comes before p3.
        # Order: p2, p1, p3
        self.assertEqual(data[0]["id"], p2.id)
        self.assertEqual(data[1]["id"], p1.id)
        self.assertEqual(data[2]["id"], p3.id)

    def test_property_invalid_ordering_field(self) -> None:
        """
        Tests that an invalid ordering field is ignored and default ordering applies.
        """
        p1 = self.create_property(
            price=100, created_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        p2 = self.create_property(
            price=200, created_at=datetime(2023, 1, 2, tzinfo=timezone.utc)
        )
        p3 = self.create_property(
            price=300, created_at=datetime(2023, 1, 3, tzinfo=timezone.utc)
        )

        # 'non_existent_field' is not in ordering_fields
        res = self.client.get(f"{self.list_url}?ordering=non_existent_field")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        p_ids = sorted([p1.id, p2.id, p3.id], reverse=True)  # Sort in descending order

        # Check the order of IDs returned by the API
        self.assertEqual(data[0]["id"], p_ids[0])
        self.assertEqual(data[1]["id"], p_ids[1])
        self.assertEqual(data[2]["id"], p_ids[2])

    def tearDown(self) -> None:
        return super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
