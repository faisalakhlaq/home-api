from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from apps.core.models import Status
from apps.properties.models import Property


class TestStatus(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.property_content_type = ContentType.objects.get_for_model(model=Property)

    def create_status(self, **kwargs) -> Status:
        payload = {
            "name": "For Sale",
            "sorting_order": 2,
            "active": True,
            "description": "Open for sale.",
            "model": self.property_content_type,
        }
        payload.update(kwargs)
        return Status.objects.create(**payload)

    def test_create_status(self) -> None:
        status = self.create_status()
        self.assertEqual(status.model, self.property_content_type)
        self.assertEqual(status.name, "For Sale")
        self.assertEqual(status.sorting_order, 2)
        self.assertEqual(status.description, "Open for sale.")
        self.assertTrue(status.active)
        self.assertIsNotNone(status.id)
