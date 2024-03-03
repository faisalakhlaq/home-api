from typing import Type, TypeVar

from django.db.models import Prefetch, QuerySet

from rest_framework.permissions import AllowAny
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Address
from apps.properties.models import Property, PropertyImage
from apps.properties.serializers import PropertyListSerializer, PropertySerializer


class PropertyViewSet(ModelViewSet):  # type: ignore
    """CRUD API for properties.

    POST Payload
    ------------
    >>> {
        "price": 10,
        "price_currency": "EUR",
        "area": 10,
        "total_area": 12,
        "measured_area": 11,
        "total_rooms": 1,
        "toilets": 1,
        "construction_year": 1900,
        "renovation_year": 1950,
        "total_floors": 1,
        "heating": "Central heating with one heating unit.",
        "outer_walls": "Brick",
        "roof_type": "Tile",
        "address": {},
        "property_images": {}
    }
    >>> Address payload within properties POST:
    {
        "street": "Some street, building number, floor 1"
        "city": "City name"
        "region": "region name"
        "postal_code": "12345"
        "country": "Country Name"
    }
    >>> Image payload within properties POST:
    {
        {
            "title": "Optional",
            "description": "Optional",
            "is_primary": false,
            "image": File,
        },
        ............,
        ............
    }

    List Response
    -------------
    A list of multiple properties is returned with all the details about each
    property along with their address details.
    >>> [
        {
            type,
            created_at,
            images,
            price,
            address:{
                zip_code,
                street,
                city,
            },
            currency,
        },
        ............,
        ............
    ]
    """

    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    _MT_co = TypeVar("_MT_co", covariant=True)

    def get_queryset(self) -> QuerySet[Property]:
        if self.action == "list":
            return Property.objects.prefetch_related(
                Prefetch(
                    "property_images",
                    queryset=PropertyImage.objects.only("image"),
                ),
                Prefetch(
                    "address",
                    queryset=Address.objects.only("postal_code", "street", "city"),
                ),
            ).only(
                "created_at",
                "price",
                "price_currency",
                "address",
            )
        else:
            return Property.objects.select_related("address").prefetch_related(
                "property_images"
            )

    def get_serializer_class(self) -> Type[BaseSerializer[_MT_co]]:
        if self.action == "list":
            return PropertyListSerializer
        else:
            return PropertySerializer
