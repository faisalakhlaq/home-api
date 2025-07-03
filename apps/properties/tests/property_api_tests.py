import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from apps.core.models import Address
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
        cls.list_url: str = reverse("apps.properties:properties-list")
        cls.detail_url: str = "apps.properties:properties-detail"
        cls.property_form: str = reverse(
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
        self.assertQuerysetEqual(queryset, expected_queryset, transform=lambda x: x)

        # Test authenticated case
        request.user = self.user
        queryset = view.get_queryset()
        expected_queryset = property_list_queryset(user_id=self.user.id)
        self.assertQuerysetEqual(queryset, expected_queryset, transform=lambda x: x)

    def test_property_create(self):
        self.client.force_authenticate(user=self.user)

        payload = {**self.property_payload, "address": self.address_payload}
        res = self.client.post(self.list_url, data=payload, format="json")
        response_data = res.json()
        print(response_data)
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

    # def test_get_create_property_form_data(self)->None:
    #     # create related objects
    #     status = create_test_status()
    #     genre = create_test_genre()
    #     cities = create_cities()
    #     res = self.client.get(self.property_form)
    #     self.assertEqual(res.status_code, 200)
    #     genre_serializer = IdNameListSerializer(
    #     Genre.objects.only('id', 'name').order_by('name').values('id', 'name'), many=True)
    #     status_serializer = IdNameListSerializer(
    #     Status.objects.only('id', 'name').order_by('name').values('id', 'name'), many=True)
    #     self.assertEqual(res.data['types'], genre_serializer.data)
    #     self.assertEqual(res.data['status'], status_serializer.data)
    #     self.assertEqual(res.data['cities'], City.objects.only('name').values_list('name', flat=True))
    #     status.delete()
    #     genre.delete()
    #     City.objects.filter(id__in=[ci.id for ci in cities]).delete()

    def tearDown(self) -> None:
        return super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
