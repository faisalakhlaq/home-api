from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from apps.core.models import Genre
from apps.properties.models import Property


class TestGenre(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.propertyCT = ContentType.objects.get_for_model(model=Property)

    def create_genre(self, **kwargs) -> Genre:
        payload = {
            "name": "Appartment",
            "sorting_order": 2,
            "active": True,
            "description": "An appartment in a building.",
            "model": self.property_content_type,
        }
        payload.update(kwargs)
        return Genre.objects.create(**payload)

    def test_create_genre(self) -> None:
        genre = self.create_genre()
        self.assertEqual(genre.model, self.propertyCT)
        self.assertEqual(genre.name, "Appartment")
        self.assertEqual(genre.sorting_order, 2)
        self.assertEqual(genre.description, "An appartment in a building.")
        self.assertTrue(genre.active)
        self.assertIsNotNone(genre.id)
