from typing import Type, TypeVar

from django_filters import rest_framework as filters

from django.db.models import Prefetch, QuerySet

from rest_framework.permissions import AllowAny
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Address
from apps.properties.models import Property, PropertyImage
from apps.properties.serializers import PropertyListSerializer, PropertySerializer


class PropertyFilter(filters.FilterSet):  # type: ignore
    """Filtering for `Property` objects.

    city: {baseurl}/api/v1/properties/properties/?city=New+York
    genre: ={baseurl}/api/v1/properties/properties/?genre=1
    type: ={baseurl}/api/v1/properties/properties/?type=Townhouse
    country: ={baseurl}/api/v1/properties/properties/?country=MyCountry
    """

    city = filters.CharFilter(field_name="address__city", lookup_expr="iexact")
    country = filters.CharFilter(field_name="address__country", lookup_expr="iexact")
    type = filters.CharFilter(field_name="type__name", lookup_expr="iexact")
    genre = filters.NumberFilter(field_name="type", lookup_expr="exact")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_area = filters.NumberFilter(field_name="area", lookup_expr="gte")
    max_area = filters.NumberFilter(field_name="area", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ("total_rooms",)


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
            id,
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

    Filtering
    ---------
    Properties API supports filtering for following fields:
    1. total_rooms
    2. genre: genre is same as type but it works with ids e.g. genre=1 will
    return all all `Property` objects that have type=1
    3. type: type works with the string types
    4. city
    5. country
    """

    permission_classes = [AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter

    _MT_co = TypeVar("_MT_co", covariant=True)

    def get_queryset(self) -> QuerySet[Property]:
        if self.action == "list":
            return (
                Property.objects.select_related("type")
                .prefetch_related(
                    Prefetch(
                        "property_images",
                        queryset=PropertyImage.objects.only("image"),
                    ),
                    Prefetch(
                        "address",
                        queryset=Address.objects.only("postal_code", "street", "city"),
                    ),
                )
                .only(
                    "id",
                    "type",
                    "description",
                    "created_at",
                    "price",
                    "price_currency",
                    "address",
                )
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
