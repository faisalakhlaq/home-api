from typing import Any, Type

from django_filters import rest_framework as filters

from django.db.models import QuerySet

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from apps.core.models import City, Genre, Status
from apps.core.serializers import IdNameListSerializer
from apps.core.views import BaseAPIViewSet
from apps.properties.models import Property
from apps.properties.querysets import (
    property_list_queryset,
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


class PropertyViewSet(BaseAPIViewSet[Property]):
    """API endpoint that allows properties to be viewed or edited.

    This viewset handles comprehensive property management, including
    listing, creation, retrieval, updates, and deletion of property records.
    It supports nested creation/updates for associated addresses and images.

    For detailed information on request/response formats, filtering options,
    and available actions, please refer to the auto-generated API schema.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = PropertyFilter
    ordering_fields = [
        "id",
        "created_at",
        "price",
        "area",
        "total_rooms",
        "construction_year",
    ]

    ordering = ["-id"]

    def get_queryset(self) -> QuerySet[Property]:
        if self.action == "list":
            if hasattr(self.request, "user") and self.request.user.is_authenticated:
                return property_list_queryset(user_id=self.request.user.id)
            else:
                return property_list_queryset()
        elif self.action == "get_create_property_form_data":
            return Property.objects.none()
        else:
            return Property.objects.select_related("address").prefetch_related(
                "property_images"
            )

    def get_serializer_class(self) -> Type[ModelSerializer[Property]]:
        if self.action in [
            "list",
            "add_to_favorites",
            "user_favorite_properties",
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

    @action(
        detail=False,
        methods=["GET"],
        url_name="get-create-property-form-data",
        permission_classes=[IsAuthenticated],
    )
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
            "cities": list(
                City.objects.only("name")
                .order_by("name")
                .values_list("name", flat=True)
            ),
        }
        return Response(data=data, status=HTTP_200_OK)
