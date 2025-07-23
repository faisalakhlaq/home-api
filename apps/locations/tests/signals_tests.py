from django.test import TestCase

from apps.locations.models import City, Country
from apps.locations.signals import generate_slug


class TestSignal(TestCase):
    def test_generate_slug(self):
        country = Country.objects.create(code="DK", name="Denmark")
        city = City(name="Test City", country=country)

        self.assertEqual(city.slug, "")
        generate_slug(city)
        self.assertEqual(city.slug, "test-city")
