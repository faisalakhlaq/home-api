from typing import Any

from django.test import TestCase

from apps.core.models import City


class TestCity(TestCase):

    def create_city(self, **kwargs: Any) -> City:
        payload = {"name": "Some City", "country": "DK"}
        payload.update(kwargs)
        return City.objects.create(**payload)

    def test_create_city(self) -> None:
        city = self.create_city(name="Copenhagen")
        self.assertEqual(city.name, "Copenhagen")
        self.assertEqual(city.country, "DK")
        self.assertIsNotNone(city.id)
        city.delete()

    def test_update_city(self) -> None:
        city = self.create_city()
        self.assertEqual(city.name, "Some City")
        self.assertEqual(city.country, "DK")
        self.assertIsNotNone(city.id)
        city.name = "Copenhagen"
        city.country = "Denmark"
        city.save()
        self.assertEqual(city.name, "Copenhagen")
        self.assertEqual(city.country, "Denmark")
        city.delete()
