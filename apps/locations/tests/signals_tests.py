from django.test import TestCase

from apps.locations.models import City, Country, Location
from apps.locations.signals import generate_slug


class TestGenerateSlug(TestCase):
    def setUp(self):
        self.country = Country.objects.create(code="US", name="United States")
        self.parent_location = Location.objects.create(
            name="New York",
            location_type="region",
            slug="new-york",
            country=self.country,
        )

    def test_city_with_country(self):
        city = City(name="Springfield", country=self.country)
        generate_slug(city)
        self.assertEqual(city.slug, "springfield-us")

    def test_city_with_duplicate_name_same_country(self):
        City.objects.create(
            name="Springfield", country=self.country, slug="springfield-us"
        )
        city = City(name="Springfield", country=self.country)
        generate_slug(city)
        self.assertEqual(city.slug, "springfield-us-1")

    def test_location_with_parent(self):
        location = Location(name="Manhattan", parent=self.parent_location)
        generate_slug(location)
        self.assertEqual(location.slug, "manhattan-new-york")

    def test_location_with_duplicate_parent_slug(self):
        Location.objects.create(
            name="Manhattan",
            parent=self.parent_location,
            slug="manhattan-new-york",
            country=self.country,
        )
        location = Location(name="Manhattan", parent=self.parent_location)
        generate_slug(location)
        self.assertEqual(location.slug, "manhattan-new-york-1")

    def test_root_location_no_parent(self):
        location = Location(name="Standalone")
        generate_slug(location)
        self.assertEqual(location.slug, "standalone")

    def test_doesnt_change_existing_slug(self):
        city = City(name="Chicago", country=self.country, slug="custom-slug")
        generate_slug(city)
        self.assertEqual(city.slug, "custom-slug")

    def test_special_characters_in_name(self):
        city = City(name="San José", country=self.country)
        generate_slug(city)
        self.assertEqual(city.slug, "san-jose-us")
