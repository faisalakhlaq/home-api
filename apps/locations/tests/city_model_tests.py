from django.db import IntegrityError
from django.test import TestCase

from apps.locations.models import City, Country


class TestCityModel(TestCase):
    def setUp(self):
        self.country = Country.objects.create(code="DK", name="Denmark")
        self.city = City.objects.create(
            name="Copenhagen", country=self.country, region="Capital Region"
        )

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Copenhagen")
        self.assertEqual(self.city.country.code, "DK")
        self.assertEqual(str(self.city), "Copenhagen, Denmark")
        self.assertEqual(str(self.city.slug), "copenhagen-dk")

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name="Copenhagen", country=self.country)
