from django.urls import reverse
from django.test import TestCase

from apps.core.models import Address
from apps.properties.models import Property
from apps.properties.serializers import (
    PropertyDetailSerializer,
    PropertyListSerializer,
    PropertySerializer,
)
from apps.properties.views import PropertyViewSet


class TestPropertyAPI(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.list_url: str = reverse("apps.properties:properties-list")
        self.detail_url: str = "apps.properties:properties-detail"
        self.property_form: str = reverse(
            "apps.properties:properties-get-create-property-form-data"
        )

        self.property_payload = {
            "price": "50000",
            "price_currency": "Euro",
            "area": 110.0,
            "total_area": 130.0,
            "total_rooms": 4.0,
            "description": "Комфорен стан на адреса Маршал Тито во Кичево",
        }
        self.address_payload = {
            "street": "Maršal Tito",
            "city": "Kičevo",
            "region": "R12",
            "postal_code": "6250",
            "country": "North Mecedonia",
        }

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

    # def test_list_queryset(self):
    #     view = PropertyViewSet()
    #     view.action = "list"
    #     list_qs = view.get_queryset()
    #     TODO Use assertQuerysetEqual
    #     self.assertEqual(list_qs, PropertyListSerializer)

    # def test_property_create(self):
    # TODO LOGIN
    #     payload = dict(self.property_payload)
    #     payload["address"] = dict(self.address_payload)
    #     res = self.client.post(
    #         self.list_url, data=payload, content_type="application/json"
    #     )
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res.data["address"]["street"], "Maršal Tito")
    #     self.assertEqual(res.data["price"], 50000)
    #     self.assertEqual(res.data["price_currency"], "Euro")
    #     self.assertEqual(res.data["area"], 110.0)
    #     self.assertEqual(res.data["total_area"], 130.0)
    #     self.assertEqual(res.data["measured_area"], None)
    #     self.assertEqual(res.data["total_rooms"], 4.0)
    #     self.assertEqual(
    #         res.data["description"], "Комфорен стан на адреса Маршал Тито во Кичево"
    #     )

    # def test_delete_property_not_allowed(self) -> None:
    # TODO LOGIN
    #     prop = self.create_property()
    #     url = reverse(self.detail_url, kwargs={"pk": prop.pk})
    #     res = self.client.delete(url)
    #     self.assertEqual(res.status_code, 405)
    #     self.assertIn("`Property` deletion is not allowed.", res.data["error"])
    #     prop.delete()

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
