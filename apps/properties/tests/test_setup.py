from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APIRequestFactory

from apps.properties.models import Property, PropertyStatus, PropertyType

User = get_user_model()


class TestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

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
        cls.user = User.objects.create_user(
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
