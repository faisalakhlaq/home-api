from typing import List

from rest_framework import serializers


class PropertySearchQuerySerializer(serializers.Serializer):  # type: ignore[type-arg]
    text = serializers.CharField(
        min_length=2, required=True, help_text="Search query (min 2 characters)"
    )
    country_code = serializers.CharField(
        required=True, max_length=2, help_text="ISO 3166-1 country code"
    )
    property_types = serializers.CharField(
        required=False, help_text="Comma-separated property types to filter"
    )

    def validate_property_types(self, value: str | None) -> None | List[str]:
        if not value:
            return None
        return value.split(",")


class CitySerializer(serializers.Serializer):  # type: ignore[type-arg]
    city = serializers.CharField()
    count = serializers.IntegerField()


class StreetSerializer(serializers.Serializer):  # type: ignore[type-arg]
    street_name = serializers.CharField()
    postal_code = serializers.CharField()
    city = serializers.CharField()
    count = serializers.IntegerField()


class AddressSerializer(serializers.Serializer):  # type: ignore[type-arg]
    street_name = serializers.CharField()
    street_number = serializers.CharField()
    postal_code = serializers.CharField()
    city = serializers.CharField()


class PropertySearchResponseSerializer(serializers.Serializer):  # type: ignore[type-arg]
    cities = CitySerializer(many=True)
    streets = StreetSerializer(many=True)
    addresses = AddressSerializer(many=True)
