from django.urls import reverse

from rest_framework import status

from apps.properties.models import PropertyType

from .test_setup import TestSetUp


class TestSearchAPI(TestSetUp):
    """
    Test suite for the PropertySearchAPI endpoint.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up common test data for the entire test class.
        This is run once for the class.
        """
        super().setUpTestData()
        cls.url_name = "apps.properties:property-search"

    def setUp(self) -> None:
        """
        Set up common resources for each individual test method.
        This is run before every test.
        """
        super().setUp()
        self.search_url = reverse(self.url_name)

        # Create a user to authenticate the client
        self.client.force_authenticate(user=self.user)

    def test_search_with_invalid_query_length_returns_400(self) -> None:
        """
        Tests that a search query with a length less than 2 returns a 400 Bad Request.
        """
        query_params = {"text": "a", "country_code": "MK"}
        response = self.client.get(self.search_url, query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Ensure this field has at least 2 characters.",
            response.data["text"][0],
        )

    def test_search_with_no_matching_properties_returns_empty_lists(self) -> None:
        """
        Tests that a search with a valid query that finds no properties
        returns a 200 OK with empty lists for all result types.
        """
        self.create_property(
            city="Skopje"
        )  # Create a property, but it shouldn't match the search
        query_params = {"text": "ab", "country_code": "MK"}
        response = self.client.get(self.search_url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["cities"], [])
        self.assertEqual(data["streets"], [])
        self.assertEqual(data["addresses"], [])

    def test_search_city_with_matching_properties(self) -> None:
        """
        Tests that a search query correctly returns matching properties
        and aggregates them into the cities, streets, and addresses lists.
        """
        # Create two properties in the same city to test aggregation
        self.create_property(
            city="Kičevo",
            street_name="Maršal Tito",
            postal_code="6250",
            description="First apartment in Kičevo",
            country_code="MK",
        )
        self.create_property(
            city="Kičevo",
            street_name="Pitu Guli",
            postal_code="6250",
            description="Second apartment in Kičevo",
            country_code="MK",
        )

        # Test search with query for "ki"
        query_params = {"text": "ki", "country_code": "MK"}
        response = self.client.get(self.search_url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Assert the structure and counts
        self.assertEqual(len(data["cities"]), 1)
        self.assertEqual(data["cities"][0]["city"], "Kičevo")
        self.assertEqual(data["cities"][0]["count"], 2)

        self.assertEqual(len(data["streets"]), 0)
        self.assertEqual(len(data["addresses"]), 0)

    def test_search_street(self) -> None:
        self.create_property(
            city="Kičevo",
            street_name="Maršal Tito",
            postal_code="6250",
            description="First apartment in Kičevo",
            country_code="MK",
        )
        self.create_property(
            city="Kičevo",
            street_name="Tito",
            postal_code="6250",
            description="Second apartment in Kičevo",
            country_code="MK",
        )

        # Test search with query for "ki"
        query_params = {"text": "Ti", "country_code": "MK"}
        response = self.client.get(self.search_url, query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Assert the structure and counts
        self.assertEqual(len(data["cities"]), 0)
        self.assertEqual(len(data["streets"]), 2)
        self.assertEqual(data["streets"][0]["street_name"], "Maršal Tito")
        self.assertEqual(data["streets"][1]["street_name"], "Tito")
        self.assertEqual(len(data["addresses"]), 2)

    def test_search_with_country_code_filter(self) -> None:
        """
        Tests that the search correctly filters properties by country code.
        """
        # Create a property in North Macedonia
        self.create_property(
            city="Kičevo", country_code="MK", description="Apartment in Kičevo, MK"
        )
        # Create a property in Denmark
        self.create_property(
            city="København",
            country_code="DK",
            description="Apartment in Copenhagen, DK",
        )

        # Search for a query that matches both properties
        query_params = {"text": "Kičevo", "country_code": "MK"}
        response = self.client.get(self.search_url, query_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Assert that only the MK property is returned
        self.assertEqual(len(data["cities"]), 1)
        self.assertEqual(data["cities"][0]["city"], "Kičevo")
        self.assertEqual(data["cities"][0]["count"], 1)
        self.assertEqual(len(data["addresses"]), 0)

    def test_search_with_property_type_filter(self) -> None:
        """
        Tests that the search correctly filters properties by property type.
        """
        self.create_property(
            city="Kičevo",
            property_type=PropertyType.APARTMENT,
            description="An apartment property",
        )
        self.create_property(
            city="Kičevo",
            property_type=PropertyType.COMMERCIAL,
            description="A commercial property",
        )

        # Search for all properties but filter for only 'apartment'
        query_params = {
            "text": "Kičevo",
            "property_types": PropertyType.APARTMENT,
            "country_code": "MK",
        }
        response = self.client.get(self.search_url, query_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Assert that only the apartment is returned
        self.assertEqual(len(data["cities"]), 1)
        self.assertEqual(data["cities"][0]["city"], "Kičevo")
        self.assertEqual(data["cities"][0]["count"], 1)
        self.assertEqual(len(data["addresses"]), 0)

    def test_search_with_multiple_filters(self) -> None:
        """
        Tests that the search works with a combination of filters.
        """
        # Create a matching property
        self.create_property(
            city="Kičevo", country_code="MK", property_type=PropertyType.APARTMENT
        )
        # Create a property that only matches the query
        self.create_property(
            city="Kičevo", country_code="DK", property_type=PropertyType.CONDOMINIUM
        )

        # Search with a query that matches both, but filters
        # that will only match the first one
        query_params = {
            "text": "ki",
            "country_code": "MK",
            "property_types": PropertyType.APARTMENT,
        }
        response = self.client.get(self.search_url, query_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(len(data["cities"]), 1)
        self.assertEqual(data["cities"][0]["city"], "Kičevo")
        self.assertEqual(data["cities"][0]["count"], 1)
        self.assertEqual(len(data["addresses"]), 0)
