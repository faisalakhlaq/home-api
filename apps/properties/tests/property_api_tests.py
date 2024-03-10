from django.urls import reverse
from django.test import TestCase

from apps.properties.views import PropertyViewSet
from apps.properties.serializers import (
    PropertyDetailSerializer,
    PropertyListSerializer,
    PropertySerializer,
)


class TestPropertyAPI(TestCase):
    def test_property_list(self) -> None:
        list_url = reverse("apps.properties:properties-list")
        res = self.client.get(list_url)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_serializer(self):
        view = PropertyViewSet()
        view.action = "retrieve"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PropertyDetailSerializer)

    def test_list_serializer_class(self):
        view = PropertyViewSet()
        view.action = "list"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PropertyListSerializer)

    def test_post_serializer_class(self):
        view = PropertyViewSet()
        view.action = "create"
        serializer_class = view.get_serializer_class()
        self.assertEqual(serializer_class, PropertySerializer)

    # def test_list_queryset(self):
    #     view = PropertyViewSet()
    #     view.action = "list"
    #     list_qs = view.get_queryset()
    #     TODO Use assertQuerysetEqual
    #     self.assertEqual(list_qs, PropertyListSerializer)

    def test_property_create(self):
        payload = {
            "address": {
                "street": "Maršal Tito",
                "city": "Kičevo",
                "region": "R12",
                "postal_code": "6250",
                "country": "North Mecedonia",
            },
            "price": "50000",
            "price_currency": "Euro",
            "area": 110.0,
            "total_area": 130.0,
            "total_rooms": 4.0,
            "description": "Комфорен стан на адреса Маршал Тито во Кичево",
        }
        list_url = reverse("apps.properties:properties-list")
        res = self.client.post(list_url, data=payload, content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["address"]["street"], "Maršal Tito")
        self.assertEqual(res.data["price"], 50000)
        self.assertEqual(res.data["price_currency"], "Euro")
        self.assertEqual(res.data["area"], 110.0)
        self.assertEqual(res.data["total_area"], 130.0)
        self.assertEqual(res.data["measured_area"], None)
        self.assertEqual(res.data["total_rooms"], 4.0)
        self.assertEqual(
            res.data["description"], "Комфорен стан на адреса Маршал Тито во Кичево"
        )
