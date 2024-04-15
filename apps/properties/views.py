from typing import Any, Type, TypeVar

from django_filters import rest_framework as filters

from django.db.models import QuerySet

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
)
from rest_framework.viewsets import ModelViewSet

from apps.core.models import City, Genre, Status
from apps.core.serializers import IdNameListSerializer
from apps.users.models import UserFavoriteProperty
from apps.properties.models import Property
from apps.properties.querysets import (
    property_list_queryset,
    user_favorite_properties_qs,
)
from apps.properties.serializers import (
    PropertyDetailSerializer,
    PropertyListSerializer,
    PropertySerializer,
)


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):  # type: ignore
    pass


class CharInFilter(filters.BaseInFilter, filters.CharFilter):  # type: ignore
    pass


class PropertyFilter(filters.FilterSet):  # type: ignore
    """Filtering for `Property` objects.

    * city: {baseurl}/api/v1/properties/properties/?city=New+York
    * genre: {baseurl}/api/v1/properties/properties/?genre=1
    * type: {baseurl}/api/v1/properties/properties/?type=Townhouse
    * country: {baseurl}/api/v1/properties/properties/?country=MyCountry
    * min_price: {baseurl}/api/v1/properties/properties/?min_price=12
    * max_price: {baseurl}/api/v1/properties/properties/?max_price=23
    * min_area: {baseurl}/api/v1/properties/properties/?min_area=1234
    * max_area: {baseurl}/api/v1/properties/properties/?max_area=1234
    * total_rooms:
    """

    city = filters.CharFilter(field_name="address__city", lookup_expr="iexact")
    country = filters.CharFilter(field_name="address__country", lookup_expr="iexact")
    type = CharInFilter(field_name="type__name", lookup_expr="in")
    genre = NumberInFilter(field_name="type", lookup_expr="in")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_area = filters.NumberFilter(field_name="area", lookup_expr="gte")
    max_area = filters.NumberFilter(field_name="area", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ("total_rooms",)


class PropertyViewSet(ModelViewSet):  # type: ignore
    """CRUD API for properties.

    The viewset contains following extra actions:
    * get-create-property-form-data

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
        "property_images": []
    }
    >>> Address payload within properties POST:
    {
        "street": "Some street, building number, floor 1"
        "city": "City name"
        "region": "region name"
        "postal_code": "12345"
        "country": "Country Name"
    }
    >>> Images payload within properties POST:
    [
        {
            "title": "Optional",
            "description": "Optional",
            "is_primary": false,
            "image": File,
        },
        ............,
        ............
    ]

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
    6. min_price
    7. max_price
    8. min_area
    9. max_area

    get-create-property-form-data
    -----------------------------
    A get call that returns the data for filling the `Property` form. Returned
    data includes:
    1. Genre List[Dict[int, str]]: A list containing valid `Type` [[id, name]]
    2. City List[str]: A list of cities to select from.
    3. Status List[Dict[int, str]]: List containig valid `Status` [{id, name}]
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter

    _MT_co = TypeVar("_MT_co", covariant=True)

    def get_queryset(self) -> QuerySet[Property]:
        if self.action == "list":
            if self.request.user.is_authenticated:
                return property_list_queryset(user_id=self.request.user.id)
            else:
                return property_list_queryset()
        elif self.action in [
            "get-create-property-form-data",
            "get_create_property_form_data",
        ]:
            return Property.objects.none()
        elif self.action in [
            "user_favorite_properties",
            "user-favorite-properties",
        ]:
            return user_favorite_properties_qs(user_id=self.request.user.id)  # type: ignore
        elif self.action in ["add-to-favorites", "add_to_favorites"]:
            return Property.objects.none()
        else:
            return Property.objects.select_related("address").prefetch_related(
                "property_images"
            )

    def get_serializer_class(self) -> Type[BaseSerializer[_MT_co]]:
        if self.action in [
            "list",
            "add-to-favorites",
            "add_to_favorites",
            "user_favorite_properties",
            "user-favorite-properties",
        ]:
            return PropertyListSerializer
        elif self.action == "retrieve":
            return PropertyDetailSerializer
        else:
            return PropertySerializer

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete operation on the `Property` is not allowed."""
        return Response(
            {"error": "`Property` deletion is not allowed."},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=False, methods=["GET"], url_name="get-create-property-form-data")
    def get_create_property_form_data(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Returns the data to help create a `Property`."""
        genre_serializer = IdNameListSerializer(
            Genre.objects.only("id", "name").order_by("name").values("id", "name"),
            many=True,
        )
        status_serializer = IdNameListSerializer(
            Status.objects.only("id", "name").order_by("name").values("id", "name"),
            many=True,
        )
        data = {
            "types": genre_serializer.data,
            "status": status_serializer.data,
            "cities": City.objects.only("name").values_list("name", flat=True),
        }
        return Response(data=data, status=HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        url_name="user-favorite-properties",
        permission_classes=[IsAuthenticated],
    )
    def user_favorite_properties(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_name="add-to-favorites",
        permission_classes=[IsAuthenticated],
        name="Add to favorites",
    )
    def add_to_favorites(
        self, request: Request, pk: int, *args: Any, **kwargs: Any
    ) -> Response:
        """Add the given property to the user favorite list."""
        property_obj = get_object_or_404(Property, pk=pk)
        UserFavoriteProperty.objects.get_or_create(
            user=request.user, property=property_obj
        )
        serializer = self.get_serializer(
            property_list_queryset(
                filter=[property_obj.id], user_id=request.user.id  # type: ignore
            ).first()
        )
        return Response(data=serializer.data, status=HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_name="remove-from-favorites",
        permission_classes=[IsAuthenticated],
        name="Remove from favorites",
    )
    def remove_from_favorites(
        self, request: Request, pk: int, *args: Any, **kwargs: Any
    ) -> Response:
        """Remove the given property from the user favorite list."""
        property_obj = get_object_or_404(Property, pk=pk)
        favorite_qs = UserFavoriteProperty.objects.filter(  # type: ignore
            user=request.user, property=property_obj
        )
        if not favorite_qs.exists():
            return Response(
                data={"error": "The given property is not in user favorites."},
                status=HTTP_400_BAD_REQUEST,
            )

        favorite_qs.delete()
        return Response(status=HTTP_204_NO_CONTENT)
