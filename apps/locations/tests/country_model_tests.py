from django.db import IntegrityError
from django.test import TestCase

from apps.locations.models import Country


class TestCountryModel(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            code="DK", name="Denmark", native_name="Danmark"
        )

    def test_country_creation(self):
        self.assertEqual(self.country.code, "DK")
        self.assertEqual(str(self.country), "Denmark")

    def test_unique_constraints(self):
        with self.assertRaises(IntegrityError):
            Country.objects.create(code="DK", name="Denmark")
