import logging

from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core.serializers import ErrorResponseSerializer
from apps.properties.services.search import PropertySearch
from apps.properties.serializers import (
    PropertySearchQuerySerializer,
    PropertySearchResponseSerializer,
)

logger = logging.getLogger(__name__)


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
                required=True,
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
        request=PropertySearchQuerySerializer,
        responses={
            200: PropertySearchResponseSerializer,
            400: OpenApiResponse(
                description=_("Invalid request"),
                response=ErrorResponseSerializer,
                examples=[
                    OpenApiExample(
                        "Query too short",
                        value={"detail": "Search must be at least 2 characters"},
                    )
                ],
            ),
            500: OpenApiResponse(
                description="Server error",
                response=ErrorResponseSerializer,
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
        query_serializer = PropertySearchQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        validated_data = query_serializer.validated_data
        query = validated_data["text"]
        country_code = validated_data.get("country_code").upper()
        property_types = validated_data.get("property_types")

        try:
            results = PropertySearch.quick_search(
                query=query, country_code=country_code, property_types=property_types
            )
            response_serializer = PropertySearchResponseSerializer(results)
            return Response(response_serializer.data, status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(msg=str(ex), exc_info=ex)
            error_serializer = ErrorResponseSerializer({"detail": str(ex)})
            return Response(
                error_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
