from django.test import TestCase

from apps.locations.models import City, CityTranslation, Country


class TestCityTranslation(TestCase):
    def setUp(self):
        country = Country.objects.create(code="DK", name="Denmark")
        self.city = City.objects.create(name="København", country=country)

    def test_translation_creation(self):
        translation = CityTranslation.objects.create(
            city=self.city, language="en", translated_name="Copenhagen"
        )
        self.assertEqual(translation.translated_name, "Copenhagen")
        self.assertEqual(str(translation), "København (en): Copenhagen")
