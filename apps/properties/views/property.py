from typing import Any, Type

from django_filters import rest_framework as filters

from django.db.models import QuerySet

from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from apps.core.utils import CharInFilter, CustomFilterSet
from apps.core.views import BaseAPIViewSet
from apps.locations.models import City
from apps.properties.models import Property, PropertyStatus, PropertyType
from apps.properties.querysets import (
    property_list_queryset,
)
from apps.properties.serializers import (
    PropertyListSerializer,
    PropertySerializer,
)


class PropertyFilter(CustomFilterSet):
    """Filtering for `Property` objects.

    #### Available query parameters
    - city: Case-insensitive exact match of city name
    - country_code: Case-insensitive exact match of country code
    - property_type: Filter by one or more property types
    - status: `status` is optional, defaults to `ACTIVE`.
        Filter by one or more statuses.
    - min_price / max_price: Price range filtering
    - min_area / max_area: Area size range filtering

    #### Examples
    * city: {baseurl}/api/v1/properties/properties/?city=New+York
    * country_code: {baseurl}/api/v1/properties/properties/?country_code=MK
    * property_type: {baseurl}/api/v1/properties/properties/?property_type=Townhouse
    * min_price: {baseurl}/api/v1/properties/properties/?min_price=12
    * max_price: {baseurl}/api/v1/properties/properties/?max_price=23
    * min_area: {baseurl}/api/v1/properties/properties/?min_area=1234
    * max_area: {baseurl}/api/v1/properties/properties/?max_area=1234
    """

    city = filters.CharFilter(field_name="city", lookup_expr="iexact")
    country_code = filters.CharFilter(field_name="country_code", lookup_expr="iexact")
    property_type = CharInFilter(field_name="property_type", lookup_expr="in")
    status = CharInFilter(field_name="status", lookup_expr="in")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_area = filters.NumberFilter(field_name="area", lookup_expr="gte")
    max_area = filters.NumberFilter(field_name="area", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ("total_rooms",)

    def __init__(
        self,
        data: Any = None,
        queryset: Any = None,
        *,
        request: Any = None,
        prefix: str | None = None
    ) -> None:
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.filters["country_code"].required = True


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
        """
        Returns the base queryset for the PropertyViewSet.

        For `list` actions, this returns a filtered and annotated queryset using the helper
        `property_list_queryset` with filters for `country_code`, `status`, and optionally
        user favorites if authenticated.

        For count action we return the same queryset as list to make sure that
        the list and count use the same filtering and once the user fetches
        the, they will get the same number of results sa displayed by the
        count.

        For non-list actions, it returns:
        - An empty queryset for `get_create_property_form_data`
        - A prefetch-optimized queryset for other actions (e.g., retrieve, update)

        This ensures consistent filtering across API views and supports performance
        optimizations for listing large datasets.
        """
        if self.action in ["list", "count"]:
            country_code = self.request.GET.get("country_code")
            if not country_code:
                raise ValidationError(
                    {
                        "country_code": "This query parameter is required.",
                    },
                    code="required",
                )

            status = self.request.GET.getlist("status")
            user_id = None
            if hasattr(self.request, "user") and self.request.user.is_authenticated:
                user_id = self.request.user.id

            return property_list_queryset(
                user_id=user_id,
                country_code=country_code,
                status=status or PropertyStatus.ACTIVE,
            )
        elif self.action == "get_create_property_form_data":
            return Property.objects.none()
        else:
            return Property.objects.prefetch_related("property_images")

    def get_serializer_class(self) -> Type[ModelSerializer[Property]]:
        if self.action == "list":
            return PropertyListSerializer
        else:
            return PropertySerializer

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete operation on the `Property` is not allowed."""
        return Response(
            {"error": "`Property` deletion is not allowed."},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )

    @extend_schema(
        summary="List Properties",
        description="""
    List properties with filtering.

    - `country_code` is required in all queries
    - If `status` is not provided, defaults to `ACTIVE`
    - Other optional filters: city, property_type, price range, area range

    Example:
    `/api/v1/properties/properties/?country_code=DK&min_price=100000`
    """,
        parameters=[
            OpenApiParameter(
                name="country_code",
                description="ISO 3166-1 country code",
                required=True,
                type=str,
                default="MK",
                examples=[
                    OpenApiExample("North Mecedonia", value="MK"),
                    OpenApiExample("Denmark", value="DK"),
                ],
            ),
            *PropertyFilter.spectacular_parameters(exclude_fields=["country_code"]),
        ],
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

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
        data = {
            "types": [choice for choice in PropertyType.values],
            "status": [choice for choice in PropertyStatus.values],
            "cities": list(
                City.objects.only("name")
                .order_by("name")
                .values_list("name", flat=True)
            ),
        }
        return Response(data=data, status=HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        url_name="count",
    )
    def count(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns the number of properties that match the applied filters.

        This endpoint applies the same filtering logic as the list view. By default,
        it returns the count of active properties. If a 'status' query parameter
        is provided, the count will reflect the number of properties in the specified
        status(es).
        """
        filtered_queryset = self.filter_queryset(self.get_queryset())
        count = filtered_queryset.count()
        return Response(data={"count": count}, status=HTTP_200_OK)
