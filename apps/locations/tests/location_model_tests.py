from django.test import TestCase

from apps.locations.models import Country, Location


class TestLocationModel(TestCase):
    def setUp(self):
        self.country = Country.objects.create(code="DK", name="Denmark")
        self.region = Location.objects.create(
            name="Capital Region", location_type="region", country=self.country
        )

    def test_location_hierarchy(self):
        municipality = Location.objects.create(
            name="Copenhagen",
            location_type="municipality",
            parent=self.region,
            country=self.country,
        )
        self.assertEqual(municipality.parent.name, "Capital Region")
        self.assertEqual(municipality.country.code, "DK")
