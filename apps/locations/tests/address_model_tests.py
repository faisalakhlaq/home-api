from django.test import TestCase

from apps.locations.models import Address, City, Country


class TestAddressModel(TestCase):
    def setUp(self):
        country = Country.objects.create(code="DK", name="Denmark")
        city = City.objects.create(name="Copenhagen", country=country)
        self.address = Address.objects.create(
            street_name="Åfløjen",
            street_number="40",
            postal_code="2300",
            city=city,
        )

    def test_address_creation(self):
        self.assertEqual(self.address.street_name, "Åfløjen")
        self.assertEqual(self.address.street_number, "40")
        self.assertEqual(self.address.city.name, "Copenhagen")
        self.assertEqual(self.address.postal_code, "2300")

    def test_formatted_address(self):
        expected = "Åfløjen 40, 2300 Copenhagen, DK"
        self.assertIn(expected, self.address.formatted_address)
