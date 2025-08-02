from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import CharField as SerialzierCharField
from rest_framework.views import APIView

from apps.properties.services.search import PropertySearch


class PropertySearchAPI(APIView):
    """
    API endpoint for returning property search suggestions.

    This endpoint is used to power the frontend search bar. It returns
    suggested matches based on user input (e.g., city name, street, postal code),
    including counts for each type of result. The response format is designed
    to be similar to how different real estate platforms provide categorized
    suggestions.

    Example:
    ```
        GET /api/v1/properties/properties/search/?text=køben
        {
            "cities": [{"label": "København", "count": 1249}],
            "streets": [{"label": "Københavnsvej", "count": 10}],
            "addresses": [{"label": "2400", "count": 42}]
        }
    ```
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Property search endpoint",
        description="""Incremental property search with type filtering.
        Returns hierarchical results (cities, streets, addresses) with counts.
        All three levels are always returned, with counts representing matches
        at each level.""",
        parameters=[
            OpenApiParameter(
                name="text",
                description="Search query (min 2 characters)",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample("Example 1 (City)", value="Bo"),
                    OpenApiExample("Example 2 (City)", value="køben"),
                    OpenApiExample("Example 3 (Postal Code)", value="7000"),
                    OpenApiExample("Example 3 (Street)", value="Boris Kidrič"),
                ],
            ),
            OpenApiParameter(
                name="country_code",
                description="ISO 3166-1 country code",
                required=False,
                type=str,
                default="MK",
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample("North Mecedonia", value="MK"),
                    OpenApiExample("Denmark", value="DK"),
                    OpenApiExample("Norway", value="NO"),
                ],
            ),
            OpenApiParameter(
                name="property_types",
                description="Comma-separated property types to filter",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(
                        "Apartment and Villas and condos", value="apartment,villa,condo"
                    )
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Hierarchical search results",
                response={
                    "type": "object",
                    "properties": {
                        "cities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "city": {"type": "string"},
                                    "count": {"type": "integer"},
                                },
                            },
                        },
                        "streets": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "street_name": {"type": "string"},
                                    "postal_code": {"type": "string"},
                                    "city": {"type": "string"},
                                    "count": {"type": "integer"},
                                },
                            },
                        },
                        "addresses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "street_name": {"type": "string"},
                                    "street_number": {"type": "string"},
                                    "postal_code": {"type": "string"},
                                    "city": {"type": "string"},
                                },
                            },
                        },
                    },
                },
                examples=[
                    OpenApiExample(
                        "Successful response",
                        value={
                            "cities": [
                                {"city": "Bogdanci", "count": 2},
                                {"city": "Bogovinje", "count": 1},
                            ],
                            "streets": [
                                {
                                    "street_name": "Kej Boris Kidrič",
                                    "postal_code": "6330",
                                    "city": "Struga",
                                    "count": 2,
                                },
                                {
                                    "street_name": "Boris Kidrič",
                                    "postal_code": "2220",
                                    "city": "Probistip",
                                    "count": 1,
                                },
                                {
                                    "street_name": "Boris Kidrič",
                                    "postal_code": "1487",
                                    "city": "Dojran",
                                    "count": 1,
                                },
                            ],
                            "addresses": [
                                {
                                    "street_name": "Kej Boris Kidrič",
                                    "street_number": "23",
                                    "postal_code": "6330",
                                    "city": "Struga",
                                },
                                {
                                    "street_name": "Kej Boris Kidrič",
                                    "street_number": "45",
                                    "postal_code": "6330",
                                    "city": "Struga",
                                },
                                {
                                    "street_name": "Boris Kidrič",
                                    "street_number": "null",
                                    "postal_code": "2220",
                                    "city": "Probistip",
                                },
                                {
                                    "street_name": "Boris Kidrič",
                                    "street_number": "null",
                                    "postal_code": "1487",
                                    "city": "Dojran",
                                },
                            ],
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description=_("Invalid request"),
                response=inline_serializer(
                    name="ErrorResponse", fields={"detail": SerialzierCharField()}
                ),
                examples=[
                    OpenApiExample(
                        "Query too short",
                        value={"detail": "Search must be at least 2 characters"},
                    )
                ],
            ),
            500: OpenApiResponse(
                description="Server error",
                response=inline_serializer(
                    name="ErrorResponse", fields={"detail": SerialzierCharField()}
                ),
                examples=[
                    OpenApiExample(
                        name="Database error",
                        value={"detail": "Database connection failed"},
                    )
                ],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        query = request.query_params.get("text", "").strip()
        country_code = request.query_params.get("country_code", "DK")
        if country_code:
            country_code = country_code.upper()

        property_types = (
            request.query_params.get("property_types", "").split(",")
            if "property_types" in request.query_params
            else None
        )

        if len(query) < 2:
            return Response(
                {"detail": _("Search must be at least 2 characters")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            results = PropertySearch.quick_search(
                query=query, country_code=country_code, property_types=property_types
            )
            return Response(results, status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
